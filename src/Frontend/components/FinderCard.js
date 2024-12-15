"use client"

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import dummyImage from '@/public/chillguy.png';

export default function FinderCard({ image, name, percentage }) {
  return (
    <div className='bg-[#1E2567] w-[300px] rounded-xl p-5 flex flex-col justify-center items-center text-white m-2'>
      <div className='rounded-xl'>
          <Image
          src = {image ? image : dummyImage}
          width={250}
          height={250}
          alt="album picture"
          className='rounded-2xl h-[250px] w-[250px] object-cover'
          />    
    
      </div>
      <div className="flex justify-between w-full">
        <div className="text-lg mt-3">{name ? name : "QY"}</div>
        <div className="text-lg mt-3">{percentage ? percentage + " %" : ""}</div>        
      </div>



    </div>
  )
}