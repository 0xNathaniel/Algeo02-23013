import Image from "next/image";
import Link from 'next/link';
import Search from '@/public/search.png';
import React from 'react';
import HomeCard from "../components/HomeCard";
import Logo from '@/public/mainlogo.png';

const Dummy = [
  {
    name: "Nathaniel Jonathan Rusli",
    nim: "13523013",
    pesan: "''Saya telah menghabiskan waktu dua jam akibat bug one line of code.''",
    img: "/fotonathan.jpg",
    bg: "#1E2567",
    link: "https://www.linkedin.com/in/nathanieljr/"
  },
  {
    name: "Maheswara Bayu Kaindra",
    nim: "13523015",
    pesan: "''Kukira kusepuh ternyata kurapuh, tapi gua ganteng jadi chill aja.''",
    img: "/fotoindra.jpeg",
    bg: "#646A9F",
    link:"https://www.linkedin.com/in/maheswarakaindra/"
  },
  {
    name: "Jessica Allen",
    nim: "13523059",
    pesan: "''First time full anggota kerja, gada yang ngilang.''",
    img: "/fotoallen.jpg",
    bg: "#9CA0C7",
    link:"https://www.linkedin.com/in/jessica-allen-lim/"
  }
]

export default function Home() {
  return (
    <div className='bg-[#F5F5F5]'>
      <div  className="w-full flex flex-col text-center py-[120px] text-[#1E2567] hover:scale-110 transition-transform duration-400 ease-in-out">
        <h2 className=" text-sm sm:text-md md:text-lg lg:text-xl my-3">Tugas Besar 2</h2>
        <h1 className="text-4xl sm:text-4xl md:text-5xl lg:text-6xl my-3 font-lora-bold">Audio & Album Finder</h1>
        <h3 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl my-3">Aljabar Linear dan Geometri</h3>
      </div>

      <div className="flex flex-col space-y-5 py-10 px-[50px] sm:px-[80px] md:px-[100px] lg:px-[100px] items-center">
        <div className="flex flex-col space-y p-[80px] bg-white rounded-3xl lg:w-[1000px] drop-shadow-xl hover:scale-110 transition-transform duration-400 ease-in-out ">
          <div className="flex text-4xl sm:text-4xl md:text-4xl lg:text-5xl text-center mb-8 font-lora-bold justify-center items-center space-x-6">
            <div>About</div>
            <Image
            src = {Logo}
            width={50}
            height={50}
            className="ml-5"
            alt = 'Logo'
            />
          </div>
          <p className="text-lg sm:text-lg md:text-xl lg:text-2xl text-justify"><span className="font-bold">Broken Home</span> yang terdiri atas <span className="font-semibold">Album Picture Finder</span> dan <span className="font-bold">Music Information Retrieval</span> adalah solusi berbasis <span className="font-bold">Information Retrieval</span> yang dirancang untuk menemukan gambar album musik dan file audio yang memiliki kesamaan  dengan data yang diunggah pengguna. Aplikasi ini mengimplementasikan algoritma pemrosesan gambar dan audio untuk memfasilitasi pencarian berbasis konten.</p>
        </div>

        <Link href="/finder">
          <button className="flex hover:scale-110 transition-transform duration-400 ease-in-out text-white px-6 rounded-lg py-3 drop-shadow-lg my-10 bg-[#646A9F] hover:bg-[#1E2567] justify-center">
            <Image
              src={Search}
              width={30}
              alt="Finder"
            />
            <p className="ml-4 text-xl">Finder</p>
          </button>
        </Link>
      </div>

      <div className="p-10 max-w-[1000px] flex flex-col items-center mx-auto">
        <div className="text-4xl sm:text-4xl md:text-4xl lg:text-5xl text-center mb-4 text-[#1E2567] font-lora-bold p-5">Brought to you by...</div>
        <div className="flex flex-col justify-center items-center ">
          {Dummy.map((person, index) => (
            <HomeCard key={index} data={person} />
          ))}          
        </div>

      </div>
    </div>
  );
}
