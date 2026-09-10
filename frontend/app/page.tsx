"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [x, setX] = useState(0);
  const [y, setY] = useState(0);

  useEffect(() => {
    fetch("http://localhost:8000/position")
      .then((response) => response.json())
      .then((position) => {
        setX(position.x);
        setY(position.y);
      });
  }, []);

  return (
    <main>
      <h1>Grid Agent</h1>

      <p>
        Position: ({x}, {y})
      </p>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(5, 60px)",
          gap: "4px",
          marginTop: "20px",
        }}
      >
        {Array.from({ length: 25 }).map((_, index) => {
          const cellX = index % 5;
          const cellY = Math.floor(index / 5);

          return (
            <div
              key={index}
              style={{
                width: "60px",
                height: "60px",
                border: "1px solid #333",
              }}
            >
              {cellX === x && cellY === y ? "🟦" : ""}
            </div>
          );
        })}
      </div>
    </main>
  );
}