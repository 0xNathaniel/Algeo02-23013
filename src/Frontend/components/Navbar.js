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
        <nav className="bg-[#9CA0C7] w-full h-[70px] flex items-center justify-between px-10">
            <div className=''>
              <Image
              src = {TextLogo}
              width={200}
              alt="TextLogo"
              />
            </div>
            <div className='flex space-x-2'>
              <Link href='/' className='mx-2'>
              <button className={`flex text-white w-full rounded-md px-5 py-2 bg-[#9CA0C7] hover:bg-[#8C90BC] items-center justify-center ${pathname ==='/' ? 'bg-[#646A9F]' : 'bg-[#9CA0C7]'}`}>
                <Image
                src = {Home}
                width={30}
                alt="Home"
                />
                <p className='ml-4 text-xl hidden md:block'>Home</p>
              </button>
              </Link>

              <Link href='/finder' className='mx-2'>
              <button className={`flex text-white w-full rounded-md  px-5 py-2 bg-[#9CA0C7] hover:bg-[#8C90BC] items-center justify-center ${pathname ==='/' ? 'bg-[#9CA0C7]' : 'bg-[#646A9F]'}`}>
                <Image
                src = {Search}
                width={30}
                alt="Finder"
                />
                <p className='ml-4 text-xl hidden md:block'>Finder</p>
              </button>
              </Link>
            </div>
        </nav>
    );
}
export default Navbar;
