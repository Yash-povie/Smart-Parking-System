'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { parkingLotApi, bookingApi } from '@/lib/api';
import Link from 'next/link';

interface ParkingLot {
  id: number;
  name: string;
  address: string;
  price_per_hour: number;
}

export default function BookParkingPage() {
  const params = useParams();
  const router = useRouter();
  const id = parseInt(params.id as string);
  
  const [lot, setLot] = useState<ParkingLot | null>(null);
  const [loading, setLoading] = useState(true);
  const [booking, setBooking] = useState({
    start_time: '',
    end_time: '',
    vehicle_number: '',
    vehicle_type: 'car',
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login?redirect=/parking-lots/' + id + '/book');
      return;
    }
    loadParkingLot();
  }, [id, router]);

  const loadParkingLot = async () => {
    try {
      setLoading(true);
      const data = await parkingLotApi.getById(id);
      setLot(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load parking lot');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    setSuccess(false);

    try {
      const token = localStorage.getItem('token');
      if (!token) {
        router.push('/login');
        return;
      }

      const bookingData = {
        parking_lot_id: id,
        start_time: new Date(booking.start_time).toISOString(),
        end_time: new Date(booking.end_time).toISOString(),
        vehicle_number: booking.vehicle_number,
        vehicle_type: booking.vehicle_type,
      };

      const result = await bookingApi.create(bookingData, token);
      setSuccess(true);
      
      setTimeout(() => {
        router.push('/dashboard');
      }, 2000);
    } catch (err: any) {
      setError(err.message || 'Booking failed');
    } finally {
      setSubmitting(false);
    }
  };

  const calculateTotal = () => {
    if (!lot || !booking.start_time || !booking.end_time) return 0;
    const start = new Date(booking.start_time);
    const end = new Date(booking.end_time);
    const hours = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60));
    return hours * lot.price_per_hour;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
          <p className="mt-4 text-gray-700 font-medium">Loading...</p>
        </div>
      </div>
    );
  }

  if (!lot) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4 font-semibold">Parking lot not found</p>
          <Link href="/" className="text-blue-600 hover:underline font-medium">
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      <header className="bg-white shadow-md">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href={`/parking-lots/${id}`} className="text-blue-600 hover:underline font-medium">
            ← Back to Parking Lot
          </Link>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Book Parking</h1>
          <p className="text-gray-600 mb-6">{lot.name}</p>
          <p className="text-sm text-gray-500">{lot.address}</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-xl p-8">
          {error && (
            <div className="bg-red-50 border-2 border-red-200 text-red-700 px-6 py-4 rounded-xl mb-6">
              <p className="font-semibold">{error}</p>
            </div>
          )}

          {success && (
            <div className="bg-green-50 border-2 border-green-200 text-green-700 px-6 py-4 rounded-xl mb-6">
              <p className="font-semibold">Booking successful! Redirecting to dashboard...</p>
            </div>
          )}

          <div className="space-y-6">
            <div>
              <label htmlFor="vehicle_number" className="block text-sm font-semibold text-gray-700 mb-2">
                Vehicle Number *
              </label>
              <input
                id="vehicle_number"
                type="text"
                required
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                placeholder="e.g., MH12AB1234"
                value={booking.vehicle_number}
                onChange={(e) => setBooking({ ...booking, vehicle_number: e.target.value })}
              />
            </div>

            <div>
              <label htmlFor="vehicle_type" className="block text-sm font-semibold text-gray-700 mb-2">
                Vehicle Type *
              </label>
              <select
                id="vehicle_type"
                required
                className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                value={booking.vehicle_type}
                onChange={(e) => setBooking({ ...booking, vehicle_type: e.target.value })}
              >
                <option value="car">Car</option>
                <option value="bike">Bike</option>
                <option value="suv">SUV</option>
                <option value="truck">Truck</option>
              </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label htmlFor="start_time" className="block text-sm font-semibold text-gray-700 mb-2">
                  Start Time *
                </label>
                <input
                  id="start_time"
                  type="datetime-local"
                  required
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                  value={booking.start_time}
                  onChange={(e) => setBooking({ ...booking, start_time: e.target.value })}
                />
              </div>

              <div>
                <label htmlFor="end_time" className="block text-sm font-semibold text-gray-700 mb-2">
                  End Time *
                </label>
                <input
                  id="end_time"
                  type="datetime-local"
                  required
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition"
                  value={booking.end_time}
                  onChange={(e) => setBooking({ ...booking, end_time: e.target.value })}
                />
              </div>
            </div>

            {booking.start_time && booking.end_time && (
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-6 border-2 border-blue-200">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm text-gray-600">Price per hour</p>
                    <p className="text-2xl font-bold text-gray-900">₹{lot.price_per_hour}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-sm text-gray-600">Total Amount</p>
                    <p className="text-3xl font-bold text-blue-600">₹{calculateTotal().toFixed(2)}</p>
                  </div>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={submitting || success}
              className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold py-4 px-6 rounded-xl hover:from-blue-700 hover:to-indigo-700 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            >
              {submitting ? 'Booking...' : success ? 'Booked!' : 'Confirm Booking'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

