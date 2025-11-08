"""
Payment processing endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.booking import Booking

router = APIRouter()

try:
    import stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    STRIPE_AVAILABLE = True
except ImportError:
    STRIPE_AVAILABLE = False
except Exception:
    STRIPE_AVAILABLE = False


class PaymentIntentRequest(BaseModel):
    booking_id: int
    amount: Optional[float] = None  # If None, use booking total_price


class PaymentIntentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str


@router.post("/create-payment-intent", response_model=PaymentIntentResponse)
async def create_payment_intent(
    payment_data: PaymentIntentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create Stripe payment intent for a booking"""
    if not STRIPE_AVAILABLE or not settings.STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment service not configured"
        )
    
    # Get booking
    booking = db.query(Booking).filter(Booking.id == payment_data.booking_id).first()
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    
    if booking.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    if booking.payment_status == "paid":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already paid"
        )
    
    # Calculate amount (in cents for Stripe)
    amount = payment_data.amount or booking.total_price
    amount_cents = int(amount * 100)
    
    try:
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount_cents,
            currency="usd",
            metadata={
                "booking_id": booking.id,
                "user_id": current_user.id,
                "parking_lot_id": booking.parking_lot_id
            },
            description=f"Parking booking #{booking.id}"
        )
        
        # Update booking with payment intent ID
        booking.payment_intent_id = intent.id
        db.commit()
        
        return PaymentIntentResponse(
            client_secret=intent.client_secret,
            payment_intent_id=intent.id
        )
    
    except stripe.error.StripeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment error: {str(e)}"
        )


@router.post("/webhook")
async def stripe_webhook(
    request: dict
):
    """Handle Stripe webhook events"""
    if not STRIPE_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment service not configured"
        )
    
    # In production, verify webhook signature
    # For now, just process the event
    
    event_type = request.get("type")
    data = request.get("data", {}).get("object", {})
    
    if event_type == "payment_intent.succeeded":
        payment_intent_id = data.get("id")
        
        # Update booking payment status
        # This would typically use a database session
        # For now, return success
        
        return {"status": "processed"}
    
    return {"status": "received"}

