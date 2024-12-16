"use client"

import React from 'react';
import Image from 'next/image';
import Link from 'next/link';
import dummyImage from '@/public/dummy.png';
import PlayButton from "@/public/playbutton.png"
import PauseButton from "@/public/pausebutton.png"
import StopButton from "@/public/stopbutton.png"
import { useState  } from 'react';
import { Midi } from "@tonejs/midi";
import * as Tone from "tone";

export default function FinderCard({ image, name, percentage, audio }) {
  const [scheduleId, setScheduleId] = useState(null); // Schedule ID to stop playback
  const audioPath = `/Data/Music Dataset/${audio}`;
  const [isPlaying, setIsPlaying] = useState(false); // Tracks whether the MIDI is playing
  const [isPaused, setIsPaused] = useState(false); // Tracks whether playback is paused
  const [synth, setSynth] = useState(null); // Stores the synth instance

  const playMidi = async () => {
    if (isPlaying && !isPaused) {
      console.log("Playback is already active. Use pause or stop.");
      return;
    }

    if (isPaused) {
      // Resume playback
      Tone.Transport.start();
      setIsPlaying(true);
      setIsPaused(false);
      console.log("Resumed playback.");
      return;
    }

    try {
      // Fetch and parse the MIDI file
      const response = await fetch(audioPath);
      const arrayBuffer = await response.arrayBuffer();
      const midi = new Midi(arrayBuffer);

      console.log("Parsed MIDI:", midi);

      // Create a synth if it doesn't already exist
      const newSynth = synth || new Tone.PolySynth(Tone.Synth).toDestination();
      setSynth(newSynth);

      // Clear any previously scheduled events
      Tone.Transport.cancel();

      // Schedule notes for playback
      midi.tracks.forEach((track) => {
        track.notes.forEach((note) => {
          Tone.Transport.schedule((time) => {
            newSynth.triggerAttackRelease(note.name, note.duration, time);
          }, note.time);
        });
      });

      await Tone.start();
      Tone.Transport.start();
      setIsPlaying(true);
      setIsPaused(false);
      console.log("Playback started.");
    } catch (error) {
      console.error("Error playing MIDI:", error);
    }
  };

  const pauseMidi = () => {
    if (!isPlaying || isPaused) {
      console.log("Cannot pause; playback is not active.");
      return;
    }

    Tone.Transport.pause(); // Pause the transport
    setIsPlaying(false);
    setIsPaused(true);
    console.log("Playback paused.");
  };

  const stopMidi = () => {
    if (!isPlaying && !isPaused) {
      console.log("Cannot stop; no active playback.");
      return;
    }

    Tone.Transport.stop(); 
    Tone.Transport.cancel(); 
    setIsPlaying(false);
    setIsPaused(false);
    console.log("Playback stopped.");
  };


  return (
    <div className='bg-[#3C427D] w-[300px] rounded-2xl p-7 flex flex-col space-y-3 justify-center items-center text-white m-2 hover:scale-105 transition-transform duration-300 ease-in-out drop-shadow-xl'>
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
      <div className="flex w-full justify-between items-center">
  {/* Audio name */}
  <div>{audio ? audio : ""}</div>

  {/* Playback controls */}
  {audio && (
  <div className="flex items-center space-x-2">
    {/* Show Play Button when not playing */}
    {!isPlaying && (
      <button>
        <Image
          src={PlayButton}
          alt="Play Button"
          width={30}
          height={30}
          onClick={playMidi}
          className="cursor-pointer"
        />
      </button>
    )}

    {/* Show Pause and Stop Buttons when playing */}
    {isPlaying && (
      <div className="flex space-x-2">
        <button onClick={pauseMidi}>
          <Image
          src={PauseButton}
          alt="Pause Button"
          width={30}
          height={30}
          className="cursor-pointer"
        />
        </button>
        <button onClick={stopMidi}>
          <Image
          src={StopButton}
          alt="Pause Button"
          width={30}
          height={30}
          className="cursor-pointer"
        />
        </button>
      </div>
    )}
  </div>
)} 
</div>
    </div> 
  )
}