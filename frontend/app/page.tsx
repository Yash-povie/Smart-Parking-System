'use client';

import { useState, useEffect } from 'react';
import { parkingLotApi } from '@/lib/api';
import Link from 'next/link';
import Suggestions from '@/components/Suggestions';

interface ParkingLot {
  id: number;
  name: string;
  address: string;
  city: string;
  latitude: number;
  longitude: number;
  total_slots: number;
  available_slots: number;
  price_per_hour: number;
  safety_rating?: number;
}

export default function Home() {
  const [parkingLots, setParkingLots] = useState<ParkingLot[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadParkingLots();
  }, []);

  const loadParkingLots = async () => {
    try {
      setLoading(true);
      const data = await parkingLotApi.getAll();
      setParkingLots(data);
      setError(null);
    } catch (err: any) {
      setError(err.message || 'Failed to load parking lots');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-lg border-b-2 border-blue-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <span className="text-3xl">🚗</span>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                Smart Parking System
              </h1>
            </div>
            <nav className="flex gap-4">
              <Link href="/" className="text-gray-700 hover:text-blue-600 font-medium transition">
                Home
              </Link>
              <Link href="/login" className="text-gray-700 hover:text-blue-600 font-medium transition">
                Login
              </Link>
              <Link href="/register" className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-4 py-2 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition font-medium">
                Register
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <h2 className="text-5xl font-bold text-gray-900 mb-4">
            Find Your Perfect Parking Spot
          </h2>
          <p className="text-xl text-gray-600 mb-6">
            Discover available parking spots across India with real-time availability
          </p>
        </div>

        {/* Suggestions */}
        <div className="mb-8">
          <Suggestions />
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-4 border-blue-600 border-t-transparent"></div>
            <p className="mt-4 text-gray-600 font-medium">Loading parking lots...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border-2 border-red-200 text-red-700 px-6 py-4 rounded-xl mb-6">
            <p className="font-semibold">{error}</p>
            <button
              onClick={loadParkingLots}
              className="mt-2 text-sm underline hover:no-underline font-medium"
            >
              Try again
            </button>
          </div>
        )}

        {/* Parking Lots Grid */}
        {!loading && !error && (
          <>
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900">All Parking Lots</h3>
              <p className="text-gray-600">{parkingLots.length} locations available</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {parkingLots.length === 0 ? (
                <div className="col-span-full text-center py-12 bg-white rounded-2xl shadow-lg p-8">
                  <p className="text-gray-600 text-lg mb-2">No parking lots available</p>
                  <p className="text-sm text-gray-500">
                    Add sample data by running: <code className="bg-gray-100 px-2 py-1 rounded">cd backend && python seed_data.py</code>
                  </p>
                </div>
              ) : (
                parkingLots.map((lot) => (
                  <div
                    key={lot.id}
                    className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-all transform hover:scale-105 border-2 border-transparent hover:border-blue-300"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-1">{lot.name}</h3>
                        <p className="text-gray-600 text-sm mb-1">{lot.address}</p>
                        <p className="text-gray-500 text-xs">{lot.city}</p>
                      </div>
                      {lot.safety_rating && (
                        <div className="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-semibold">
                          ⭐ {lot.safety_rating.toFixed(1)}
                        </div>
                      )}
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div className="bg-green-50 rounded-xl p-3">
                        <p className="text-xs text-gray-600 mb-1">Available</p>
                        <p className="text-2xl font-bold text-green-600">
                          {lot.available_slots || 0}
                        </p>
                        <p className="text-xs text-gray-500">of {lot.total_slots || 0} slots</p>
                      </div>
                      <div className="bg-blue-50 rounded-xl p-3">
                        <p className="text-xs text-gray-600 mb-1">Price</p>
                        <p className="text-2xl font-bold text-blue-600">
                          ₹{lot.price_per_hour || 0}
                        </p>
                        <p className="text-xs text-gray-500">per hour</p>
                      </div>
                    </div>

                    <Link
                      href={`/parking-lots/${lot.id}`}
                      className="block w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-center py-3 rounded-xl hover:from-blue-700 hover:to-indigo-700 transition font-semibold shadow-md hover:shadow-lg"
                    >
                      View Details →
                    </Link>
                  </div>
                ))
              )}
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t-2 border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600">
            Smart Parking System - AI-Powered Parking Solution for India 🇮🇳
          </p>
        </div>
      </footer>
    </div>
  );
}
