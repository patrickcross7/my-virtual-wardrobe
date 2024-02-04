import { useEffect, useRef, useState } from "react";
import { SliderPicker } from 'react-color';
import "./DrawingPage.css";

export default function DrawingPage() {
  const canvasReference = useRef(null);
  const contextReference = useRef(null);
  const [isPressed, setIsPressed] = useState(false);
  const [currentColor, setCurrentColor] = useState("#000000");

  const clearCanvas = () => {
    const canvas = canvasReference.current;
    const context = canvas.getContext("2d");
    context.clearRect(0, 0, canvas.width, canvas.height);
  };

  const beginDraw = (x, y) => {
    contextReference.current.beginPath();
    contextReference.current.moveTo(x, y);
    setIsPressed(true);
  };

  const updateDraw = (x, y) => {
    if (!isPressed) return;
    const context = contextReference.current;
    context.lineTo(x, y);
    context.stroke();
  };

  const endDraw = () => {
    contextReference.current.closePath();
    setIsPressed(false);
  };

  const handleMouseDown = (e) => {
    const { offsetX, offsetY } = e.nativeEvent;
    beginDraw(offsetX, offsetY);
  };

  const handleMouseMove = (e) => {
    const { offsetX, offsetY } = e.nativeEvent;
    updateDraw(offsetX, offsetY);
  };

  const handleMouseUp = endDraw;

  const handleTouchStart = (e) => {
    e.preventDefault();
    const { clientX, clientY } = e.touches[0];
    const { left, top } = canvasReference.current.getBoundingClientRect();
    beginDraw(clientX - left, clientY - top);
  };

  const handleTouchMove = (e) => {
    e.preventDefault();
    const { clientX, clientY } = e.touches[0];
    const { left, top } = canvasReference.current.getBoundingClientRect();
    updateDraw(clientX - left, clientY - top);
  };

  const handleTouchEnd = endDraw;

  useEffect(() => {
    const canvas = canvasReference.current;
    const context = canvas.getContext("2d");
    canvas.width = 700;
    canvas.height = 700;
    context.lineCap = "round";
    context.lineWidth = 5;
    contextReference.current = context;
  }, []);

  useEffect(() => {
    const context = contextReference.current;
    context.strokeStyle = currentColor;
  }, [currentColor]);

  const handleColorChange = (color) => setCurrentColor(color.hex);

  const saveDrawing = () => {
    const canvas = canvasReference.current;
    const imgData = canvas.toDataURL("image/png");
    const link = document.createElement("a");
    link.href = imgData;
    link.download = "drawing.png";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="container">
      <canvas
        ref={canvasReference}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      />
      <div className="color-picker">
        <SliderPicker color={currentColor} onChange={handleColorChange} />
      </div>
      <div className="buttons">
        <button onClick={clearCanvas}>Clear</button>
        <button onClick={saveDrawing}>Save</button>
      </div>
    </div>
  );
}