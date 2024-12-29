"use client";

import Image from "next/image";
import { WaitForUserInput } from "./WaitForUserInput";

export default function Home() {
  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20">
      {/* Header */}
      <header className="flex flex-col items-center gap-4">
        <Image
          className="dark:invert"
          src="/learnmate-logo.svg"
          alt="LearnMate logo"
          width={180}
          height={38}
          priority
        />
        <h1 className="text-3xl sm:text-4xl font-bold text-center sm:text-left">
          Welcome to LearnMate - Your Personalized Study Assistant
        </h1>
      </header>

      {/* Main Content */}
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <p className="text-lg text-center sm:text-left max-w-2xl">
          LearnMate helps you create and manage customized study plans, track your progress, 
          and receive valuable feedback. Start improving your learning journey today!
        </p>

        {/* Integrating WaitForUserInput component */}
        <WaitForUserInput />
      </main>

      {/* Footer */}
      <footer className="row-start-3 flex gap-6 flex-wrap items-center justify-center mt-10">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://learnmate.com/learn"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn More
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://learnmate.com/examples"
          target="_blank"
          rel="noopener noreferrer"
        >
          Explore Examples
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://learnmate.com"
          target="_blank"
          rel="noopener noreferrer"
        >
          Visit LearnMate
        </a>
      </footer>
    </div>
  );
}
