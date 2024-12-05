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

  return (
    <div>
      <div className='bg-[#1E2567] text-white h-full p-10 flex flex-col justify-center items-center'>
        <h1 className='text-4xl font-lora-bold'>Upload Here!</h1>
        <FinderCard data={Uploaded[0]} />

        <form action="/upload" method="post" encType="multipart/form-data" className='flex  items-center'>
          <input type="file" name="file" />
          
          <div>
            <button type="submit" className='bg-[#855738] p-2 m-2 rounded-lg'>Submit</button> 
          </div>
        </form>

        <div className='text-2xl'>
          <button className='bg-[#F4992A] hover:bg-[#F3C081] p-2 px-5 m-2 rounded-lg'>Audios</button>
          <button className='bg-[#F4992A] hover:bg-[#F3C081] p-2 px-5 m-2 rounded-lg'>Pictures</button>
          <button className='bg-[#F4992A] hover:bg-[#F3C081] p-2 px-5 m-2 rounded-lg'>Mapper</button>
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
              <FinderCard key={index} data={data} />
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
