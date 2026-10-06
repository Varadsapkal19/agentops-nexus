"use client";

import { useEffect, useState, useRef } from "react";

export function useAnimatedCounter(end: number, duration: number = 1500) {
  const [count, setCount] = useState(0);
  const frameRef = useRef<number>(0);

  useEffect(() => {
    let startTime: number | null = null;
    const startValue = 0;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // cubic ease-out
      setCount(Math.floor(startValue + (end - startValue) * eased));

      if (progress < 1) {
        frameRef.current = requestAnimationFrame(animate);
      }
    };

    frameRef.current = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frameRef.current);
  }, [end, duration]);

  return count;
}

export function useTypingEffect(text: string, speed: number = 40) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    setDisplayed("");
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) {
        setDisplayed(text.slice(0, i + 1));
        i++;
      } else {
        clearInterval(interval);
      }
    }, speed);
    return () => clearInterval(interval);
  }, [text, speed]);

  return displayed;
}

export function useTimeAgo(date: Date) {
  const [timeAgo, setTimeAgo] = useState("");

  useEffect(() => {
    const update = () => {
      const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
      if (seconds < 60) setTimeAgo(`${seconds}s ago`);
      else if (seconds < 3600) setTimeAgo(`${Math.floor(seconds / 60)}m ago`);
      else if (seconds < 86400) setTimeAgo(`${Math.floor(seconds / 3600)}h ago`);
      else setTimeAgo(`${Math.floor(seconds / 86400)}d ago`);
    };
    update();
    const interval = setInterval(update, 10000);
    return () => clearInterval(interval);
  }, [date]);

  return timeAgo;
}
