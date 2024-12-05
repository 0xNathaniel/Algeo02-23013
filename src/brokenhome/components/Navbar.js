"use client"
import React from 'react';
import Link from 'next/link';
import TextLogo from '@/public/textlogo.png';
import Image from 'next/image'
import Home from '@/public/home.png';
import Search from '@/public/search.png';
import { usePathname } from 'next/navigation';

const Navbar = () => {
  const pathname = usePathname();
    return (
        <nav className="bg-[#646A9F] w-full h-[70px] flex items-center justify-between px-10">
            <div className=''>
              <Image
              src = {TextLogo}
              width={200}
              alt="TextLogo"
              />
            </div>
            <div className='flex '>
              <Link href='/'>
              <button className={`flex text-white w-full rounded-md px-5 py-2 mx-2 bg-[#646A9F] hover:bg-[#F3C081] items-center justify-center ${pathname ==='/' ? 'bg-[#F4992A]' : 'bg-[#646A9F]'}`}>
                <Image
                src = {Home}
                width={30}
                alt="Home"
                />
                <p className='ml-4 text-2xl hidden md:block'>Home</p>
              </button>
              </Link>

              <Link href='/finder'>
              <button className={`flex text-white w-full rounded-md  px-5 py-2 mx-2 bg-[#646A9F] hover:bg-[#F3C081] items-center justify-center ${pathname ==='/' ? 'bg-[#646A9F]' : 'bg-[#F4992A]'}`}>
                <Image
                src = {Search}
                width={30}
                alt="Finder"
                />
                <p className='ml-4 text-2xl hidden md:block'>Finder</p>
              </button>
              </Link>
            </div>
        </nav>
    );
}
export default Navbar;
