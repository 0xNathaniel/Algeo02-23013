"use client";

import React, { useState } from "react";
import Image from "next/image";
import FinderCard from "@/components/FinderCard";
import Left from "@/public/panahkiri.png";
import Right from "@/public/panahkanan.png";
import axios from "axios";

const ITEMS_PER_PAGE = 6;

const page = () => {
  const [currentPage, setCurrentPage] = useState(0);
  const [albumResponse, setAlbumResponse] = useState([]); // Album results (image similarity)
  const [midiResponse, setMidiResponse] = useState([]); // Music results (MIDI similarity)
  const [currentView, setCurrentView] = useState("album"); // Default view: album
  const [file, setFile] = useState(null); // File to be uploaded
  const [zipFile, setZipFile] = useState(null); // ZIP file to be uploaded
  const [mapperFile, setMapperFile] = useState(null); // Mapper file to be uploaded
  const [message, setMessage] = useState(null);

  // Handle Pagination: Previous Page
  const handlePrevious = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  // Handle Pagination: Next Page
  const handleNext = () => {
    const totalItems =
      currentView === "album" ? albumResponse.length : midiResponse.length;
    if ((currentPage + 1) * ITEMS_PER_PAGE < totalItems) {
      setCurrentPage(currentPage + 1);
    }
  };

  // Paginated data for current view
  const paginatedData =
    currentView === "album"
      ? albumResponse.slice(
          currentPage * ITEMS_PER_PAGE,
          (currentPage + 1) * ITEMS_PER_PAGE
        )
      : midiResponse.slice(
          currentPage * ITEMS_PER_PAGE,
          (currentPage + 1) * ITEMS_PER_PAGE
        );

  // Handle Single File Upload (Image or MIDI)
  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file.");
      return;
    }

    const formData = new FormData();
    const fileExtension = file.name.split(".").pop().toLowerCase();

    try {
      if (["jpg", "jpeg", "png"].includes(fileExtension)) {
        // API for images
        formData.append("query_image", file);

        const response = await axios.post("http://localhost:8000/finder/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        const result = response.data.similar_images;
        setAlbumResponse(result);
        setMessage("Image file processed successfully!");
      } else if (["mid", "midi"].includes(fileExtension)) {
        // API for MIDI files
        formData.append("query_midi", file);

        const response = await axios.post("http://localhost:8000/music/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        const result = response.data.similar_audio_files;
        setMidiResponse(result);
        setMessage("MIDI file processed successfully!");
      } else {
        setMessage("Unsupported file type. Please upload an image or MIDI file.");
      }
    } catch (error) {
      setMessage(
        error.response?.data?.detail || "An error occurred while uploading the file."
      );
    }
  };

  // Handle ZIP File Upload (Picture/Audio)
  const handleZipUpload = async (type) => {
    if (!zipFile) {
      setMessage("Please select a ZIP file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", zipFile);

    try {
      await axios.post("http://localhost:8000/upload-zip/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage(`${type} ZIP file uploaded successfully!`);
    } catch (error) {
      setMessage("An error occurred while uploading the ZIP file.");
    }
  };

  // Handle Mapper File Upload
  const handleMapperUpload = async () => {
    if (!mapperFile) {
      setMessage("Please select a mapper file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", mapperFile);

    try {
      await axios.post("http://localhost:8000/upload-mapper/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage("Mapper file uploaded successfully!");
    } catch (error) {
      setMessage("An error occurred while uploading the mapper file.");
    }
  };

  const handleFileChange = (event) => setFile(event.target.files[0]);
  const handleZipFileChange = (event) => setZipFile(event.target.files[0]);
  const handleMapperFileChange = (event) => setMapperFile(event.target.files[0]);

  return (
    <div>
      {/* Upload Section */}
      <div className="bg-[#1E2567] text-white h-full p-10 flex flex-col justify-center items-center">
        <h1 className="text-4xl font-lora-bold">Upload Here!</h1>
        <FinderCard image={file ? URL.createObjectURL(file) : null} name={file?.name || "No file selected"} />

        {/* Upload Form */}
        <form onSubmit={handleUpload} className="flex items-center gap-2 mb-2">
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#855738] hover:file:bg-[#F3C081]"
          />
          <button
            type="submit"
            className="py-2 px-4 my-2 bg-[#855738] text-white font-semibold rounded-lg shadow-md hover:bg-[#F3C081]"
          >
            Upload
          </button>
        </form>
        <div className="flex space-x-6">
          {/* ZIP Upload Form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleZipUpload("Picture");
            }}
            className="flex space-x-4 items-center"
          >
            <input
              type="file"
              onChange={handleZipFileChange}
              accept=".zip"
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#855738] hover:file:bg-[#F3C081]"
            />
            <button
              type="submit"
              className="py-2 px-4 my-2 bg-[#F4992A] text-white rounded-lg shadow-md hover:bg-[#F3C081]"
            >
              Pictures
            </button>
          </form>

          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleZipUpload("Audio");
            }}
            className="flex space-x-4 items-center"
          >
            <input
              type="file"
              onChange={handleZipFileChange}
              accept=".zip"
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#855738] hover:file:bg-[#F3C081]"
            />
            <button
              type="submit"
              className="py-2 px-4 my-2 bg-[#F4992A] text-white rounded-lg shadow-md hover:bg-[#F3C081]"
            >
              Audios
            </button>
          </form>

          {/* Mapper Upload Form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleMapperUpload();
            }}
            className="flex space-x-4 items-center"
          >
            <input
              type="file"
              onChange={handleMapperFileChange}
              accept=".txt"
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#855738] hover:file:bg-[#F3C081]"
            />
            <button
              type="submit"
              className="py-2 px-4 bg-[#F4992A] text-white rounded-lg shadow-md hover:bg-[#F3C081]"
            >
              Mapper
            </button>
          </form>
        </div>

        
      </div>

      {/* Results Header */}
      <div className="bg-[#F4992A] h-[120px] flex items-center justify-center text-5xl text-white font-lora-bold">
        Results
      </div>

      {/* Results Section */}
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

        {/* Paginated Results */}
        <div className="flex flex-wrap items-center justify-center">
          {currentView === "album" ? (
            albumResponse.length > 0 ? (
              paginatedData.map((data, index) => (
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
          ) : midiResponse.length > 0 ? (
            paginatedData.map((data, index) => (
              <FinderCard
              key={index}
              image={`/Data/Dataset/${data.midi_name}`}
              name={data.midi_name}
              percentage={data.similarity_percentage}
            />
            ))
          ) : (
            <p className="text-lg mt-3">No music results to display</p>
          )}
        </div>

        {/* Pagination Controls */}
        <div className="flex">
          <button className="m-3" onClick={handlePrevious} disabled={currentPage === 0}>
            <Image src={Left} width={20} alt="arrow" />
          </button>
          <div className="m-3 text-xl">
            {currentPage + 1} of{" "}
            {Math.ceil(
              currentView === "album" ? albumResponse.length /ITEMS_PER_PAGE : midiResponse.length /ITEMS_PER_PAGE
            )}
          </div>
          <button
            className="m-3"
            onClick={handleNext}
            disabled={
              (currentPage + 1) * ITEMS_PER_PAGE >=
              (currentView === "album" ? albumResponse.length : midiResponse.length)
            }
          >
            <Image src={Right} width={20} alt="arrow" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default page;
