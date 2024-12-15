"use client"

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import dummyImage from '@/public/chillguy.png';
import PlayButton from "@/public/playbutton.png"

export default function FinderCard({ image, name, percentage, audio }) {
  return (
    <div className='bg-[#3C427D] w-[300px] rounded-2xl p-7 flex flex-col justify-center items-center text-white m-2'>
      <div className='rounded-2xl'>
          <Image
          src = {image ? image : dummyImage}
          width={350}
          height={250}
          alt="album picture"
          className='rounded-2xl h-[200px] w-[350px] object-cover'
          />    
      </div>
      <div className="flex justify-between w-full">
        <div className="text-lg mt-3">{name ? name : "File name unknown"}</div>
        <div className="text-lg mt-3">{percentage ? percentage + " %" : ""}</div>        
      </div>
      <div className='flex w-full justify-between'>
        <div>{audio ? audio : "File name unknown"}</div>
        <div>
          <Image
          src = {PlayButton}
          alt='Play Button'
          width={30}
          height={30}
          />
        </div>
      </div>

    </div>
  )
}