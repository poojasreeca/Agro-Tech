import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Camera, Upload, Calendar, Tractor, ShoppingCart } from 'lucide-react';

const AgroTechApp = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [diseaseResult, setDiseaseResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      const formData = new FormData();
      formData.append('image', file);

      try {
        const response = await fetch('http://localhost:5000/api/detect-disease', {
          method: 'POST',
          body: formData,
        });
        const result = await response.json();
        setDiseaseResult(result);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold text-center mb-8">Agro Tech</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Disease Detection Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Camera className="w-6 h-6" />
              Leaf Disease Detection
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input
                type="file"
                accept="image/*"
                onChange={handleImageUpload}
                className="w-full"
              />
              {loading && <p>Analyzing image...</p>}
              {diseaseResult && (
                <div className="mt-4">
                  <p className="font-semibold">Result:</p>
                  <p>Disease: {diseaseResult.disease}</p>
                  <p>Confidence: {(diseaseResult.confidence * 100).toFixed(2)}%</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Soil Test Appointment Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="w-6 h-6" />
              Book Soil Test
            </CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4">
              <Input placeholder="Name" />
              <Input type="email" placeholder="Email" />
              <Input type="tel" placeholder="Phone" />
              <Input type="date" />
              <Button className="w-full">Book Appointment</Button>
            </form>
          </CardContent>
        </Card>

        {/* Machinery Rental Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Tractor className="w-6 h-6" />
              Rent Machinery
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <select className="w-full p-2 border rounded">
                <option>Select Machinery Type</option>
                <option>Tractor</option>
                <option>Harvester</option>
                <option>Seeder</option>
              </select>
              <Input type="date" placeholder="From Date" />
              <Input type="date" placeholder="To Date" />
              <Button className="w-full">Check Availability</Button>
            </div>
          </CardContent>
        </Card>

        {/* Online Trading Card */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <ShoppingCart className="w-6 h-6" />
              Online Trading
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Input placeholder="Search Products" />
              <div className="h-48 overflow-y-auto border rounded p-2">
                <div className="space-y-2">
                  {/* Sample products */}
                  <div className="flex justify-between items-center">
                    <span>Organic Rice</span>
                    <Button size="sm">Buy</Button>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Fresh Vegetables</span>
                    <Button size="sm">Buy</Button>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default AgroTechApp;
