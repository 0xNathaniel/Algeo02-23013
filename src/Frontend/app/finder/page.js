"use client";

import React, { useRef, useState } from "react";
import Image from "next/image";
import FinderCard from "@/components/FinderCard";
import Left from "@/public/panahkiri.png";
import Right from "@/public/panahkanan.png";
import axios from "axios";
import Dummy from "@/public/dummy.png"

const ITEMS_PER_PAGE = 8;

const page = () => {
  const [currentPage, setCurrentPage] = useState(0);
  const [albumResponse, setAlbumResponse] = useState([]); 
  const [midiResponse, setMidiResponse] = useState([]); 
  const [currentView, setCurrentView] = useState("album"); 
  const [file, setFile] = useState(null); 
  const [imageFile, setImageFile] = useState(null); 
  const [audioFile, setAudioFile] = useState(null); 
  const [mapperFile, setMapperFile] = useState(null); 
  const [message, setMessage] = useState(null);
  const [executionTime, setExecutionTime] = useState(null); 
  const [imagePreview, setImagePreview] = useState(null); 
  const [isRecording, setIsRecording] = useState(false);
  const [audioURL, setAudioURL] = useState(null);
  const [uploadMessage, setUploadMessage] = useState(null);
  const [audioPath, setAudioPath] = useState(null);



  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setFile(selectedFile);

    if (selectedFile) {
      const fileExtension = selectedFile.name.split(".").pop().toLowerCase();
      if (["jpg", "jpeg", "png"].includes(fileExtension)) {
        setImagePreview(URL.createObjectURL(selectedFile));
      } else if (["mid", "midi"].includes(fileExtension)) {
        setImagePreview(Dummy);
      } else {
        setImagePreview(null);
      }
    } else {
      setImagePreview(null);
    }
  };

  const handlePrevious = () => {
    if (currentPage > 0) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNext = () => {
    const totalItems =
      currentView === "album" ? albumResponse.length : midiResponse.length;
    if ((currentPage + 1) * ITEMS_PER_PAGE < totalItems) {
      setCurrentPage(currentPage + 1);
    }
  };

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
        formData.append("query_image", file);

        const response = await axios.post("http://localhost:8000/image/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        const result = response.data.similar_images;
        setAlbumResponse(result);
        setExecutionTime(response.data.execution_time);
        setMessage("Image file processed successfully!");
      } else if (["mid", "midi"].includes(fileExtension)) {
        formData.append("query_midi", file);

        const response = await axios.post("http://localhost:8000/music/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        const result = response.data.similar_audio_files;
        setAudioPath(response.data.file_url); 
        setMidiResponse(result);
        setExecutionTime(response.data.execution_time);
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

  const handleImageUpload = async () => {
    if (!imageFile) {
      setMessage("Please select an image file.");
      return;
    }
  
    const formData = new FormData();
    formData.append("files", imageFile); 
  
    try {
      const response = await axios.post("http://localhost:8000/upload-images/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
  
      setMessage(response.data.message || "Image file uploaded successfully!");
      console.log("Uploaded Images:", response.data.processed_files);
    } catch (error) {
      if (error.response) {
        console.error("Server Error:", error.response.data);
        setMessage(error.response.data.detail || "Error uploading the image file.");
      } 
    }
  };
  
  
  const handleAudioUpload = async () => {
    if (!audioFile) {
      setMessage("Please select an audio file.");
      return;
    }
  
    const formData = new FormData();
    formData.append("files", audioFile); 
  
    try {
      const response = await axios.post("http://localhost:8000/upload-music/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
  
      setMessage(response.data.message || "Audio file uploaded successfully!");
      console.log("Uploaded Audios:", response.data.processed_files);
    } catch (error) {
      if (error.response) {
        console.error("Server Error:", error.response.data);
        setMessage(error.response.data.detail || "Error uploading the audio file.");
      }
    }
  };
  
  const handleMapperUpload = async () => {
    if (!mapperFile) {
      setMessage("Please select a mapper file.");
      return;
    }

    const formData = new FormData();
    formData.append("files", mapperFile);

    try {
      await axios.post("http://localhost:8000/upload-mapper/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      setMessage("Mapper file uploaded successfully!");
    } catch (error) {
      setMessage("An error occurred while uploading the mapper file.");
    }
  };

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);


  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = (event) => {
      audioChunksRef.current.push(event.data);
    };

    mediaRecorder.onstop = () => {
      const audioBlob = new Blob(audioChunksRef.current, { type: "audio/webm" });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioURL(audioUrl);
      audioChunksRef.current = [];

      uploadAudio(audioBlob);
    };

    mediaRecorder.start();
    mediaRecorderRef.current = mediaRecorder;
    setIsRecording(true);
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const uploadAudio = async (audioBlob) => {
    const formData = new FormData();
    formData.append("file", audioBlob, "recording.webm");
  
    try {
      const response = await axios.post("http://127.0.0.1:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadMessage(response.data.message);
    } catch (error) {
      setUploadMessage("Upload failed. Please try again.");
      console.error(error);
    }
  };
  
  const handleImageFileChange = (event) => setImageFile(event.target.files[0]);
  const handleAudioFileChange = (event) => setAudioFile(event.target.files[0]);
  const handleMapperFileChange = (event) => setMapperFile(event.target.files[0]);

  
  return (
    <div className="bg-[#F5F5F5] pt-[50px]">
      {/* Upload Section */}
      <div className=" bg-white mx-[50px] sm:mx-[50px] md:mx-[50px] lg:mx-[100px] text-[#1E2567] h-full shadow-lg mb-10 rounded-xl p-10 flex flex-col justify-center items-center">
        <h1 className="text-4xl font-lora-bold mb-6">Upload Here!</h1>
        <FinderCard
          image={imagePreview}
          name={file?.name || "No file selected"}
          audio = {audioPath ? audioPath : ""}
        />

        <div className="p-4 flex flex-col items-center justify-center hover:scale-110 transition-transform duration-400 ease-in-out">
          <button
            onClick={isRecording ? stopRecording : startRecording}
            className={`px-4 py-2  rounded-lg shadow-md ${
              isRecording ? "bg-[#D1D3E3] text-[#1E2567]" : "bg-[#1E2567] text-white"
            }`}
          >
            {isRecording ? "Stop Recording" : "Start Recording"}
          </button>

          {audioURL && (
              <div className="mt-4">
                <div className="font-semibold">Recorded Audio:</div>
                <audio controls src={audioURL}></audio>
              </div>
            )}
            {uploadMessage && <p className="mt-4">{uploadMessage}</p>}
        </div>

        <div>or</div>

        {/* Upload Form */}
        <form onSubmit={handleUpload} className="flex items-center gap-2 mb-2 hover:scale-110 transition-transform duration-400 ease-in-out">
          <input
            type="file"
            onChange={handleFileChange}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#1E2567] hover:file:bg-[#E7E7EB]"            
          />
          <button
            type="submit"
            className="py-2 px-4 my-2 bg-[#1E2567] text-white rounded-lg shadow-md hover:bg-[#646A9F]"
          >
            Upload
          </button>
        </form>

        <div className="flex flex-wrap md:flex-row lg:flex-nowrap space-x-6 items-center justify-center">
          {/* Pictures Dataset Form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleImageUpload("Picture");
            }}
            className="flex space-x-4 items-center hover:scale-110 transition-transform duration-400 ease-in-out"
          >
            <input
              type="file"
              onChange={handleImageFileChange}
              name="files[]"
              multiple
              accept="image/*,video/*"
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#1E2567] hover:file:bg-[#E7E7EB]"
            />
            <button
              type="submit"
              className="py-2 px-4 my-2 bg-[#646A9F] text-white rounded-lg shadow-md hover:bg-[#1E2567]"
            >
              Pictures
            </button>
          </form>
          
          {/* Audios Dataset Form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleAudioUpload("Audio");
            }}
            className="flex space-x-4 items-center hover:scale-110 transition-transform duration-400 ease-in-out"
          >
            <input
              type="file"
              onChange={handleAudioFileChange}
              name="files[]"
              multiple
              accept=".mid, .midi"
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#1E2567] hover:file:bg-[#E7E7EB]"
            />
            <button
              type="submit"
              className="py-2 px-4 my-2 bg-[#646A9F] text-white rounded-lg shadow-md hover:bg-[#1E2567]"
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
            className="flex space-x-4 items-center hover:scale-110 transition-transform duration-400 ease-in-out"
          >
            <input
              type="file"
              onChange={handleMapperFileChange}
              accept=".txt"
              className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-white file:text-[#1E2567] hover:file:bg-[#E7E7EB]"
            />
            <button
              type="submit"
              className="py-2 px-4 my-2 bg-[#646A9F] text-white rounded-lg shadow-md hover:bg-[#1E2567]"
            >
              Mapper
            </button>
          </form>
        </div>

        
      </div>

      {/* Results Header */}
      <div className="bg-[#646A9F] mt-10 mx-[50px] md:mx-[200px] shadow-lg rounded-2xl h-[60px] md:h-[80px] flex items-center justify-center text-xl sm:text-2xl md:text-3xl lg:text-4xl text-white font-lora-bold">
        Here are the results!
      </div>

      {/* Results Section */}
      <div className="py-10  text-white flex flex-col space-y-4 items-center justify-center">
        <div className="text-2xl flex space-x-4">
          <button
            className={`py-2 px-5 rounded-lg hover:scale-110 transition-transform duration-400 ease-in-out ${
              currentView === "album" ? "bg-[#1E2567]" : "bg-[#646A9F]"
            }`}
            onClick={() => setCurrentView("album")}
          >
            Album
          </button>
          <button
            className={`py-2 px-5 rounded-lg hover:scale-110 transition-transform duration-400 ease-in-out ${
              currentView === "music" ? "bg-[#1E2567]" : "bg-[#646A9F]"
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
                  image={`/Data/Album Dataset/${data.pic_name}`}
                  name={data.audio_name}
                  percentage={data.similarity_percentage}
                  audio={data.audio_file}
                />
              ))
            ) : (
              <p className="text-lg mt-3 text-[#1E2567]">No album results to display</p>
            )
          ) : midiResponse.length > 0 ? (
            paginatedData.map((data, index) => (
              <FinderCard
              key={index}
              image={`/Data/Album Dataset/${data.pic_name}`}
              name={data.audio_name}
              percentage={data.similarity_percentage}
              audio={data.audio_file}
            />
            ))
          ) : (
            <p className="text-lg mt-3 text-[#1E2567]">No music results to display</p>
          )}
        </div>

        {/* Pagination Controls */}
        <div className="flex text-[#1E2567]">
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

        {currentView === "album" ? (
          <div className="flex space-x-10 text-[#1E2567]">
            <div>Total Output: {albumResponse.length}</div>
            <div>Processing Time: {executionTime ? executionTime.toFixed(2) : "-"} s</div>
          </div>
        ) : (
          <div className="flex space-x-10 text-[#1E2567]">
            <div>Total Output: {midiResponse.length}</div>
            <div>Processing Time: {executionTime ? executionTime.toFixed(2) : "-"} s</div>
          </div>
        )}
      </div>
    </div>
  );
};

export default page;