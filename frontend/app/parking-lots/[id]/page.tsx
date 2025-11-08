'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { parkingLotApi, parkingSlotApi, aiApi } from '@/lib/api';
import Link from 'next/link';

interface ParkingLot {
  id: number;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  total_slots: number;
  available_slots: number;
  price_per_hour: number;
  description?: string;
}

interface ParkingSlot {
  id: number;
  slot_number: string;
  status: 'available' | 'occupied' | 'reserved';
}

export default function ParkingLotDetailPage() {
  const params = useParams();
  const id = parseInt(params.id as string);
  
  const [lot, setLot] = useState<ParkingLot | null>(null);
  const [slots, setSlots] = useState<ParkingSlot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, [id]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [lotData, slotsData] = await Promise.all([
        parkingLotApi.getById(id),
        parkingSlotApi.getByLotId(id),
      ]);
      setLot(lotData);
      setSlots(slotsData);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load parking lot details');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
          <p className="mt-4 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  if (error || !lot) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Parking lot not found'}</p>
          <Link href="/" className="text-blue-600 hover:underline">
            Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <Link href="/" className="text-blue-600 hover:underline">
            ← Back to Home
          </Link>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{lot.name}</h1>
          <p className="text-gray-600 mb-4">{lot.address}</p>
          
          {lot.description && (
            <p className="text-gray-700 mb-4">{lot.description}</p>
          )}

          <div className="grid grid-cols-3 gap-4 mt-6">
            <div className="text-center">
              <p className="text-sm text-gray-500">Total Slots</p>
              <p className="text-2xl font-bold text-gray-900">{lot.total_slots}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">Available</p>
              <p className="text-2xl font-bold text-green-600">{lot.available_slots}</p>
            </div>
            <div className="text-center">
              <p className="text-sm text-gray-500">Price</p>
              <p className="text-2xl font-bold text-gray-900">₹{lot.price_per_hour}/hr</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Parking Slots</h2>
          {slots.length === 0 ? (
            <p className="text-gray-600">No slots available</p>
          ) : (
            <div className="grid grid-cols-4 md:grid-cols-8 gap-2">
              {slots.map((slot) => (
                <div
                  key={slot.id}
                  className={`p-3 rounded text-center text-sm font-medium ${
                    slot.status === 'available'
                      ? 'bg-green-100 text-green-800'
                      : slot.status === 'occupied'
                      ? 'bg-red-100 text-red-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}
                >
                  {slot.slot_number}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl shadow-xl p-6 text-white">
          <h3 className="text-xl font-bold mb-4">Ready to Book?</h3>
          <p className="mb-4">Reserve your parking spot now and save time!</p>
          <Link
            href={`/parking-lots/${id}/book`}
            className="inline-block bg-white text-blue-600 font-bold py-3 px-6 rounded-xl hover:bg-gray-100 transition shadow-lg"
          >
            Book Now →
          </Link>
        </div>
      </main>
    </div>
  );
}

