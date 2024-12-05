"use client"
import React from 'react';
import Image from 'next/image';

export default function HomeCard({ data }) {
  return (
    <div className="bg-[#F3C081] h-full mx-[0px] my-[50px] rounded-2xl py-[50px] px-20 flex flex-col md:flex-row items-center max-w-[1200px] justify-center">
      <div className="flex-shrink-0 w-[300px] h-[250px] overflow-hidden rounded-2xl">
        <Image
          src={data.img}
          width={300}
          height={300}
          alt="Orang Baik"
          className="rounded-2xl object-cover w-full h-full"
        />
      </div>
      {/* Text Content */}
      <div className="flex flex-col justify-center px-5 md:px-10">
        <div className="text-4xl font-semibold py-5">{data.name}</div>
        <div className="text-2xl font-semibold">{data.nim}</div>
        <div className="text-xl">{data.pesan}</div>
      </div>
    </div>
  );
};
