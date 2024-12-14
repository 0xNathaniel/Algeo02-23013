"use client"

import React from 'react'
import Image from 'next/image'
import FinderCard from '@/components/FinderCard'
import { useState } from 'react';
import Left from '@/public/panahkiri.png';
import Right from '@/public/panahkanan.png';

const generateDummyDataAudio = () => {
  const data = [];
  for (let i = 1; i <= 59; i++) {
    data.push({
      name: `blabla${i}.midi`,
      img: "/chillguy.png"
    });
  }
  return data;
};

const generateDummyDataPicture = () => {
  const data = [];
  for (let i = 1; i <= 59; i++) {
    data.push({
      name: `blabla${i}.png`,
      img: "/chillguy.png"
    });
  }
  return data;
};

let Dummy = generateDummyDataAudio();

const Uploaded = [
  {
    name: 'blablahey.midi',
    img: '/chillguy.png'
  }
]

const page = () => {
const ITEMS_PER_PAGE = 6;

const [currentPage, setCurrentPage] = useState(0);

const handlePrevious = () => {
  if (currentPage > 0) {
    setCurrentPage(currentPage - 1);
  }
};

const handleNext = () => {
  if ((currentPage + 1) * ITEMS_PER_PAGE < Dummy.length) {
    setCurrentPage(currentPage + 1);
  }
};

const paginatedData = Dummy.slice(currentPage * ITEMS_PER_PAGE, (currentPage + 1) * ITEMS_PER_PAGE);
  const setDummyData = (type) => {
    setCurrentPage(0); // Reset to first page when data type changes
    if (type === 'audio') {
      Dummy = generateDummyDataAudio();
    } else if (type === 'picture') {
      Dummy = generateDummyDataPicture();
    }
  };

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState();


  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage('Please select a file.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/finder/', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      if (response.ok) {
        setMessage(`File uploaded successfully: ${result.path}`);
      } else {
        setMessage(`Upload failed: ${result.message}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setMessage('An error occurred while uploading the file.');
    }
  };

  const [uploadedImage, setUploadedImage] = useState(null); // State for the image URL
  const [imageName, setImageName] = useState(); // State for the image name

  const handleFileChange = (event) => {
    const file = event.target.files[0]; // Get the first file
    if (file) {
      setImageName(file.name); // Set the image name
      const reader = new FileReader();
      reader.onload = (e) => {
        setUploadedImage(e.target.result); // Update state with file URL
      };
      reader.readAsDataURL(file); // Read file as a URL
    }
  };

  return (
    <div>
      <div className='bg-[#1E2567] text-white h-full p-10 flex flex-col justify-center items-center'>
        <h1 className='text-4xl font-lora-bold'>Upload Here!</h1>
        <FinderCard image={uploadedImage} name={imageName} />
        <form onSubmit={handleUpload} className="flex items-center gap-2 mb-2">
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#855738] hover:file:bg-[#F3C081]"
          />
          <button
            type="submit"
            className="py-2 px-4 my-2 bg-[#855738] text-white font-semibold rounded-lg shadow-md hover:bg-[#F3C081] focus:outline-none focus:ring-2 focus:ring-[#F4992A] focus:ring-offset-2"
          >
            Upload
        </button>
      </form>

        <div className='text-2xl flex space-x-2'>
          <button className='bg-[#F4992A] hover:bg-[#F3C081] py-2 px-5 rounded-lg'>Audios</button>
          <button className='bg-[#F4992A] hover:bg-[#F3C081] py-2 px-5 rounded-lg'>Pictures</button>
          <button className='bg-[#F4992A] hover:bg-[#F3C081] py-2 px-5 rounded-lg'>Mapper</button>
        </div>
      </div>

      <div className='bg-[#F4992A] h-[120px] flex items-center justify-center text-5xl text-white font-lora-bold'>
        Results
      </div>

      <div className='bg-[#F3C081] py-10 md:px-[250px] text-white flex flex-col items-center justify-center'>
          <div>
            <button className='bg-[#1E2567] hover:bg-[#646A9F] p-2 px-5 m-2 rounded-lg text-2xl' onClick={() => setDummyData('picture')}>Album</button>
            <button className='bg-[#1E2567] hover:bg-[#646A9F] p-2 px-5 m-2 rounded-lg text-2xl' onClick={() => setDummyData('audio')}>Music</button>
          </div>
          <div className='flex flex-wrap items-center justify-center'>
            {paginatedData.map((data, index) => (
              <FinderCard key={index} image={data.img} name={data.name}/>
            ))}
          </div>

          <div className='flex'>
            <button className='m-3' onClick={handlePrevious} disabled={currentPage === 0}>
              <Image
              src = {Left}
              width={20}
              alt = 'arrow'
              />
            </button>
            <div className='m-3 text-xl'>
              {currentPage + 1} of {Math.ceil(Dummy.length / ITEMS_PER_PAGE)}
            </div>
            <button className='m-3' onClick={handleNext} disabled={(currentPage + 1) * ITEMS_PER_PAGE >= Dummy.length}>
              <Image
              src = {Right}
              width={20}
              alt = 'arrow'
              />
            </button>
          </div>
      </div>
    </div>
  )
}

export default page
