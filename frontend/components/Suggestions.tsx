'use client';

import { useState, useEffect } from 'react';
import { parkingLotApi } from '@/lib/api';
import Link from 'next/link';

interface ParkingLot {
  id: number;
  name: string;
  address: string;
  price_per_hour: number;
  available_slots: number;
  total_slots: number;
  safety_rating: number;
}

export default function Suggestions() {
  const [suggestions, setSuggestions] = useState<ParkingLot[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSuggestions();
  }, []);

  const loadSuggestions = async () => {
    try {
      setLoading(true);
      const lots = await parkingLotApi.getAll();
      // Sort by availability and rating, take top 3
      const sorted = lots
        .filter((lot: ParkingLot) => lot.available_slots > 0)
        .sort((a: ParkingLot, b: ParkingLot) => {
          const scoreA = (a.available_slots / a.total_slots) * a.safety_rating;
          const scoreB = (b.available_slots / b.total_slots) * b.safety_rating;
          return scoreB - scoreA;
        })
        .slice(0, 3);
      setSuggestions(sorted);
    } catch (err) {
      console.error('Failed to load suggestions:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">💡 Suggestions</h3>
        <p className="text-gray-600">Loading suggestions...</p>
      </div>
    );
  }

  if (suggestions.length === 0) {
    return null;
  }

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl shadow-lg p-6 border-2 border-purple-200">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">💡</span>
        <h3 className="text-xl font-bold text-gray-900">Recommended for You</h3>
      </div>
      <p className="text-sm text-gray-600 mb-4">Based on availability and safety ratings</p>
      
      <div className="space-y-3">
        {suggestions.map((lot) => (
          <Link
            key={lot.id}
            href={`/parking-lots/${lot.id}`}
            className="block bg-white rounded-xl p-4 hover:shadow-md transition-all border-2 border-transparent hover:border-purple-300"
          >
            <div className="flex justify-between items-start">
              <div className="flex-1">
                <h4 className="font-semibold text-gray-900 mb-1">{lot.name}</h4>
                <p className="text-sm text-gray-600 mb-2">{lot.address}</p>
                <div className="flex gap-4 text-sm">
                  <span className="text-green-600 font-medium">
                    {lot.available_slots} available
                  </span>
                  <span className="text-yellow-600 font-medium">
                    ⭐ {lot.safety_rating?.toFixed(1) || 'N/A'}
                  </span>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-purple-600">₹{lot.price_per_hour}/hr</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

