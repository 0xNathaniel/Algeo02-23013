"use client";

import React from "react";
import Image from "next/image";
import FinderCard from "@/components/FinderCard";
import { useState } from "react";
import Left from "@/public/panahkiri.png";
import Right from "@/public/panahkanan.png";
import axios from "axios"; 

const generateDummyDataAudio = () => {
  const data = [];
  for (let i = 1; i <= 59; i++) {
    data.push({
      name: `blabla${i}.midi`,
      img: "/chillguy.png",
    });
  }
  return data;
};

const generateDummyDataPicture = () => {
  const data = [];
  for (let i = 1; i <= 59; i++) {
    data.push({
      name: `blabla${i}.png`,
      img: "/chillguy.png",
    });
  }
  return data;
};

let Dummy = generateDummyDataAudio();


const page = () => {
  const ITEMS_PER_PAGE = 6;

  const [currentPage, setCurrentPage] = useState(0);
  const [albumResponse, setAlbumResponse] = useState([]); // State for image similarity results
  const [midiResponse, setMidiResponse] = useState([]); // State for MIDI similarity results
  const [currentView, setCurrentView] = useState("album"); // Default to Album view



  const handlePrevious = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNext = () => {
    if ((currentPage + 1) * ITEMS_PER_PAGE < result.length) {
      setCurrentPage(currentPage + 1);
    }
  };

  const [file, setFile] = useState(null);
  const [message, setMessage] = useState(null);
  console.log("HALOOOO HEY STUPIDDDDDDDD");

  const handleUpload = async (e) => {
    e.preventDefault();
    console.log("handleUpload triggered");
  
    if (!file) {
      setMessage("Please select a file.");
      return;
    }
  
    const formData = new FormData();
    formData.append("query_image", file);
  
    try {
      // Call the first API (image similarity)
      const imageResponse = await axios.post("http://localhost:8000/finder/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      const imageResult = imageResponse.data.similar_images;
      console.log("Image API Response:", imageResult);
      setAlbumResponse(imageResult);
  
      // Call the second API (MIDI similarity)
      const midiFormData = new FormData();
      midiFormData.append("query_midi", file); // Reuse the same file (or another file if applicable)
  
      const midiResponse = await axios.post("http://localhost:8000/music/", midiFormData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
  
      const midiResult = midiResponse.data.similar_audio_files;
      console.log("MIDI API Response:", midiResult);
      setMidiResponse(midiResult); // Create a new state for MIDI results if needed
  
      setMessage("File uploaded successfully!");
    } catch (error) {
      console.error("Upload error:", error);
      setMessage(
        error.response?.data?.detail || "An error occurred while uploading the file."
      );
    }
  };
  

  const [apiResponse, setApiResponse] = useState([]);
    const paginatedData = apiResponse.slice(
    currentPage * ITEMS_PER_PAGE,
    (currentPage + 1) * ITEMS_PER_PAGE
  );
  

  const [uploadedImage, setUploadedImage] = useState(null); // State for the image URL
  const [imageName, setImageName] = useState(); // State for the image name

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFile(file); // Update the file state
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
      <div className="bg-[#1E2567] text-white h-full p-10 flex flex-col justify-center items-center">
        <h1 className="text-4xl font-lora-bold">Upload Here!</h1>
        <FinderCard image={uploadedImage} name={imageName} />

        <form onSubmit={handleUpload} className="flex items-center gap-2 mb-2" autoComplete="off">
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#855738] hover:file:bg-[#F3C081]"
            autoComplete="off"
          />
          <button
            type="submit"
            className="py-2 px-4 my-2 bg-[#855738] text-white font-semibold rounded-lg shadow-md hover:bg-[#F3C081] focus:outline-none focus:ring-2 focus:ring-[#F4992A] focus:ring-offset-2"
          >
            Upload
          </button>
        </form>

        <div className="text-2xl flex space-x-2">
          <button className="bg-[#F4992A] hover:bg-[#F3C081] py-2 px-5 rounded-lg">Audios</button>
          <button className="bg-[#F4992A] hover:bg-[#F3C081] py-2 px-5 rounded-lg">Pictures</button>
          <button className="bg-[#F4992A] hover:bg-[#F3C081] py-2 px-5 rounded-lg">Mapper</button>
        </div>
      </div>

      <div className="bg-[#F4992A] h-[120px] flex items-center justify-center text-5xl text-white font-lora-bold">
        Results
      </div>

      <div className="bg-[#F3C081] py-10 md:px-[250px] text-white flex flex-col items-center justify-center">
      <div className="text-2xl flex space-x-2">
        <button
          className={`py-2 px-5 rounded-lg ${
            currentView === "album" ? "bg-[#F4992A]" : "bg-[#F3C081]"
          }`}
          onClick={() => setCurrentView("album")}
        >
          Album
        </button>
        <button
          className={`py-2 px-5 rounded-lg ${
            currentView === "music" ? "bg-[#F4992A]" : "bg-[#F3C081]"
          }`}
          onClick={() => setCurrentView("music")}
        >
          Music
        </button>
      </div>

      <div className="flex flex-wrap items-center justify-center">
        {currentView === "album" ? (
          albumResponse && albumResponse.length > 0 ? (
            albumResponse.map((data, index) => (
              <FinderCard
                key={index}
                image={`/Data/Dataset/${data.pic_name}`}
                name={data.pic_name}
                percentage={data.similarity_percentage}
              />
            ))
          ) : (
            <p className="text-lg mt-3">No album results to display</p>
          )
        ) : currentView === "music" ? (
          midiResponse && midiResponse.length > 0 ? (
            midiResponse.map((data, index) => (
              <div key={index} className="p-4 border rounded-lg">
                <p>Rank: {data.rank}</p>
                <p>MIDI Name: {data.midi_name}</p>
                <p>Similarity: {data.similarity}%</p>
              </div>
            ))
          ) : (
            <p className="text-lg mt-3">No music results to display</p>
          )
        ) : null}
      </div>

          

        <div className="flex">
          <button 
            className="m-3" 
            onClick={handlePrevious} 
            disabled={currentPage === 0}>
            <Image src={Left} width={20} alt="arrow" />
          </button>
          <div className="m-3 text-xl">
            {currentPage + 1} of {Math.ceil(apiResponse.length / ITEMS_PER_PAGE)}
          </div>
          <button
            className="m-3"
            onClick={handleNext}
            disabled={(currentPage + 1) * ITEMS_PER_PAGE >= apiResponse.length}
          >
            <Image src={Right} width={20} alt="arrow" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default page;
