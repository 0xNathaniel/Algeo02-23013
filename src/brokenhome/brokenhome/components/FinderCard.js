"use client"

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

export default function FinderCard({ data }) {
  return (
    <div className='bg-[#1E2567] w-[310px] rounded-xl p-5 flex flex-col justify-center items-center text-white m-8'>
      <div className='rounded-xl'>
        <Image
        src = {data.img}
        width={250}
        height={250}
        alt="album picture"
        className='rounded-xl'
        />        
      </div>

      <div className='text-2xl mt-3'>{data.name}</div>

    </div>
  )
}