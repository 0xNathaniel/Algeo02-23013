import Image from "next/image";
import Link from 'next/link';
import Search from '@/public/search.png';
import React from 'react';
import HomeCard from "../components/HomeCard";
import Logo from '@/public/mainlogo.png';

const Dummy = [
  {
    name: "Nathaniel Jonathan Ruslim",
    nim: "13519013",
    pesan: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat",
    img: "/chillguy.png"
  },
  {
    name: "Maheswara Bayu Kaindra",
    nim: "13519013",
    pesan: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat",
    img: "/chillguy.png"
  },
  {
    name: "Jessica Allen",
    nim: "13519013",
    pesan: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec purus feugiat",
    img: "/chillguy.png"
  }
]

export default function Home() {
  return (
    <div className=''>
      <div  className="w-full flex flex-col text-center py-[120px] bg-[#1E2567] text-white">
        <h2 className="text-xl my-3">Tugas Besar 2</h2>
        <h1 className="text-6xl my-3 font-lora-bold">Audio & Album Finder</h1>
        <h3 className="text-4xl my-3">Aljabar Linear dan Geometri</h3>
      </div>

      <div className="flex flex-col bg-[#F4992A] p-10 sm:px-[100px] md:px-[100px] lg:px-[250px] items-center">
        <div className=" p-[80px] bg-[#F3C081] rounded-3xl lg:w-[1000px]">
          <div className="flex text-5xl text-center mb-8 font-lora-bold justify-center">
            <div>About</div>
            <Image
            src = {Logo}
            width={50}
            className="ml-5"
            />
          </div>
          <p className="text-2xl">Broken home adalah lorem ipsum des morales imaculata es spanyol ula to se u fskd sog  sdjsdjfnan dfksklorem ipsum des morales imaculata es spanyol ula to se u fskd sog  sdjsdjfnan dfksklorem ipsum des morales imaculata es spanyol ula to se u fskd sog  sdjsdjfnan dfksklorem ipsum des morales imaculata es spanyol ula to se u fskd sog  sdjsdjfnan dfksk</p>
        </div>
        <Link href='/finder'>
          <button className='flex text-white w-[200px] rounded-md px-5 py-3 my-10 bg-[#855738] hover:bg-[#1E2567] justify-center'>
            <Image
            src = {Search}
            width={30}
            alt="Finder"
            />
            <p className='ml-4 text-2xl'>Finder</p>
          </button>
        </Link>
      </div>

      <div className="bg-[#1E2567] p-10">
        <div className="text-5xl text-center mb-4 text-white font-lora-bold p-5">Brought to you by...</div>
        <div className="flex flex-col justify-center items-center">
          {Dummy.map((person, index) => (
            <HomeCard key={index} data={person} />
          ))}          
        </div>

      </div>
    </div>
  );
}
