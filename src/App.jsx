import React, { useState } from "react";

export default function CO2EmissionCalculator() {
  const [inputs, setInputs] = useState({
    energy_kwh: "",
    transport_km: "",
    waste_kg: "20",
  });

  const [emission, setEmission] = useState(null);
  const [isCalculating, setIsCalculating] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setInputs({ ...inputs, [e.target.name]: e.target.value });
  };

  const calculateEmission = async () => {
    setIsCalculating(true);
    setError(null); // Reset error on new calculation

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputs),
      });

      const data = await response.json();
      if (response.ok) {
        setEmission(data.predicted_emission_kg);
      } else {
        setError(data.error || "An error occurred");
      }
    } catch (err) {
      setError("Failed to connect to the server");
    } finally {
      setIsCalculating(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white flex items-center justify-center p-4 animate-fade-in">
      <div className="w-full max-w-md rounded-3xl bg-gradient-to-tr from-gray-800 to-gray-900 p-8 shadow-[0_20px_50px_rgba(0,255,170,0.1)] border border-green-500 animate-glow">
        <h2 className="text-4xl font-extrabold text-center mb-8 text-green-400 animate-bounce-slow">🌿 CO₂ Emission Calculator</h2>
        <div className="space-y-6">
          <div className="group">
            <label className="block mb-1 text-sm font-medium text-gray-300">Energy Usage (kWh)</label>
            <input
              name="energy_kwh"
              value={inputs.energy_kwh}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-400 transition duration-300 group-hover:scale-105"
              type="number"
              placeholder="e.g. 100"
            />
          </div>
          <div className="group">
            <label className="block mb-1 text-sm font-medium text-gray-300">Transport Distance (km)</label>
            <input
              name="transport_km"
              value={inputs.transport_km}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-400 transition duration-300 group-hover:scale-105"
              type="number"
              placeholder="e.g. 50"
            />
          </div>
          <div className="group">
            <label className="block mb-1 text-sm font-medium text-gray-300">Waste Generated (kg)</label>
            <input
              name="waste_kg"
              value={inputs.waste_kg}
              onChange={handleChange}
              className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-green-400 transition duration-300 group-hover:scale-105"
              type="number"
            />
          </div>
          <button
            onClick={calculateEmission}
            disabled={isCalculating}
            className="w-full bg-green-500 hover:bg-green-600 disabled:opacity-50 text-white font-semibold py-3 px-6 rounded-xl transition-transform duration-300 transform hover:scale-105"
          >
            {isCalculating ? "Calculating..." : "Calculate Emissions"}
          </button>
          {emission !== null && (
            <div className="mt-6 text-center text-xl animate-fade-in">
              Predicted CO₂ Emission: <span className="text-green-300 font-bold">{emission} kg</span>
            </div>
          )}
          {error && (
            <div className="mt-6 text-center text-xl text-red-500 animate-fade-in">
              Error: <span className="font-bold">{error}</span>
            </div>
          )}
        </div>
      </div>
      <style jsx>{`
        .animate-fade-in {
          animation: fadeIn 1s ease-in-out;
        }

        .animate-glow {
          animation: glowPulse 3s ease-in-out infinite;
        }

        .animate-bounce-slow {
          animation: bounce 2s infinite;
        }

        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }

        @keyframes glowPulse {
          0% { box-shadow: 0 0 15px rgba(0,255,170,0.2); }
          50% { box-shadow: 0 0 25px rgba(0,255,170,0.4); }
          100% { box-shadow: 0 0 15px rgba(0,255,170,0.2); }
        }

        @keyframes bounce {
          0%, 100% { transform: translateY(0); }
          50% { transform: translateY(-8px); }
        }
      `}</style>
    </div>
  );
}
