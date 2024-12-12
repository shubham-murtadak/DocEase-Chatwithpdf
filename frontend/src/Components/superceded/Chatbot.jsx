import React from "react";
import { Box, Button, Input, Text, Flex } from "@chakra-ui/react";
import { ArrowUpIcon } from "@chakra-ui/icons"; // Add this import
import { useState } from "react";
import axios from "axios";
import { FcUpload } from "react-icons/fc";
import { FaVolumeUp } from 'react-icons/fa';
import { FaMicrophone } from 'react-icons/fa';
import styled, { keyframes, css } from "styled-components";
import robo from "../Images/robot.png"
import loading from "../Images/loading.gif"

export const Chatbot = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isAnimationActive, setIsAnimationActive] = useState(false);
  const [chooseName, setChooseName] = useState(null);
  const [userMessage, setUserMessage] = useState("");
  const [chatResult, setChatResult] = useState([]);
  const [isChatFormVisible, setIsChatFormVisible] = useState(false);
  const [visibleName,setVisibleName] = useState(null)
  const [isLoading, setIsLoading] = useState(false);
  


  console.log(isAnimationActive);
  console.log(selectedFile, "selectedFile");
  console.log(chooseName);
  console.log("res", chatResult);
  console.log("visibleName", visibleName)


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selectedFile) {
      setIsAnimationActive(false);
      setTimeout(() => {
        setIsAnimationActive(true);
      }, 0);

      setTimeout(() => {
        setChooseName("File Uploaded");
        setIsChatFormVisible(true);
        setVisibleName(chooseName)
      }, 7000);
      const formData = new FormData();
      formData.append("file", selectedFile);
      try {
        const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        });
        console.log(res.data);
        const { original_filename, file_path } = res.data;
        console.log("Original Filename:", original_filename);
        console.log("Unique Filename:", file_path);
        setSelectedFile(file_path);
      } catch (error) {
        console.log(error);
      }
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setSelectedFile(file);
    setChooseName(file.name);
  };

  const handleSubmitChat = async (e) => {
    e.preventDefault();

    setIsLoading(true);
    setUserMessage("")

    try {
      let res = await axios.post("http://127.0.0.1:5000/chat", {
        query: userMessage,
        file_path: selectedFile ? `${selectedFile}` : null,
      });
      console.log("Response from server:", res);
      const chatReply = await res.data.result;
      console.log("Chat Reply:", chatReply);

      const updatedConversation = [
        ...chatResult,
        { role: "user", content: userMessage },
        { role: "bot", content: chatReply },
      ];

      setChatResult(updatedConversation);
      console.log("Updated Chat Reply:", updatedConversation);
      setIsLoading(false);
    } catch (error) {
      console.log(error.message);
    }
  };
  const handleVoiceInput = () => {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; // Set the language
    recognition.interimResults = false; // Set interim results
    recognition.maxAlternatives = 1; // Set the maximum number of alternatives
  
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript; // Get the recognized text
      setUserMessage(transcript); // Set the recognized text to the userMessage state
    };
  
    recognition.onerror = (event) => {
      console.error("Speech recognition error: ", event.error);
    };
  
    recognition.start(); // Start the voice recognition
  };
  

    // Function to handle text-to-speech
    const handleTextToSpeech = (text) => {
      const utterance = new SpeechSynthesisUtterance(text);
      speechSynthesis.speak(utterance);
    };


  return (
  //   <Flex h="100vh" bg="#F8F0E5">
  // {/* PDF upload section */}
  // <Flex
  //   pos="relative"
  //   bg="#0F2C59"
  //   p="2px"
  //   w="15%" // Reduced width of the PDF upload section
  //   direction={"column"}
  //   // align={"top"}
  //   align={"center"}
  //   shadow="rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px;"
  // >
  //   {/* <Text
  //     fontSize={"6xl"}
  //     color="#DAC0A3"
  //     fontFamily={"'Lilita One', cursive"}
  //   >
  //     DocEase
  //   </Text> */}

  //   <form action="" onSubmit={handleSubmit} style={{ margin: "auto" }}>
  //     <Text
  //       pos="absolute"
  //       left="50%"
  //       top="45%"
  //       transform={"translate(-50%)"}
  //       zIndex="3"
  //       fontSize={"xl"}
  //       fontFamily={"'Lilita One', cursive"}
  //     >
  //       {chooseName ? chooseName : "Choose File"}
  //     </Text>
  //     <LoadingStyle isAnimationActive={isAnimationActive}>
  //       <Box
  //         pos={"absolute"}
  //         left="50%"
  //         top="5%"
  //         transform="translate(-50%)"
  //         borderRadius="30%"
  //         border="2px dashed #0F2C59"
  //         w="90%"
  //         h="90%"
  //         m="auto"
  //       ></Box>
  //       <Input
  //         border="1px solid red"
  //         opacity="0"
  //         type="file"
  //         top="0%"
  //         w="100%"
  //         h="100%"
  //         borderRadius={"30%"}
  //         accept=".pdf"
  //         onChange={handleFileChange}
  //         cursor="pointer"
  //       />
  //     </LoadingStyle>
  //     <Button bg="#DAC0A3" mt="10px" type="submit">
  //       Upload
  //     </Button>
  //   </form>
  // </Flex>

  

  // {/* Chat section */}
  <Flex h="100vh" bg="#F8F0E5">
  {/* Chat History Section */}
  <Flex
    bg="#0F2C59"
    p="4"
    w="20%"
    borderRadius="md"
    direction="column"
    align="center"
    shadow="rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px;"
  >
    {/* Chat History Section */}
    <Box flex="1" mb="2">
      <Text fontSize="2xl" color="white" mb="2" textAlign="center">
        Chat History
      </Text>
      <Box
        overflowY="scroll"
        maxH="50vh" // Adjusted height to fit half
        w="100%"
        borderRadius="md"
        bg="#EADBC8"
        p="2"
      >
        {/* Display chat history messages here */}
        {chatResult.map((message, index) => (
          <Text key={index} color="black" mb="2">
            {message.role === "user" ? "You: " : "Bot: "}
            {message.content}
          </Text>
        ))}
      </Box>
    </Box>

    {/* PDF History Section */}
    <Box flex="1">
      <Text fontSize="2xl" color="white" mb="2" textAlign="center">
        PDF History
      </Text>
      <Box
        overflowY="scroll"
        maxH="50vh" // Adjusted height to fit half
        w="100%"
        borderRadius="md"
        bg="#EADBC8"
        p="2"
      >
        {/* Display PDF history entries here */}
        <Text color="black">No PDFs uploaded yet.</Text>
      </Box>
    </Box>
  </Flex>


  <Flex direction={"column"} w="70%" m="auto" gap="35">
    <Box textAlign={"left"} pl="25px" fontSize={"xl"} fontFamily={"'Lilita One', cursive"}>
      {/* {visibleName} */}
    </Box>

    <Box
      bottom={0}
      bg="#EADBC8"
      h="80vh"
      w="75vw"
      borderRadius="90px"
      pos="fixed"
      // pos="relative"
      boxShadow="rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px;"
    >
      <img
        style={{
          position: "absolute",
          opacity: "0.1",
          left: "50%",
          top: "50%",
          transform: "translate(-50%,-50%)",
        }}
        src={robo}
        alt=""
      />
  {/* Header Section */}
<Box
  position="fixed"  // Set position to fixed to stick to the top
  top="0"           // Align to the very top of the viewport
  left="80"          // Align to the very left of the viewport
  right="30"         // Stretch to the very right of the viewport
  bg="skin"      // Background color of the header
  p="0px"          // Padding for the header
  color="#DAC0A3"   // Text color
  fontSize="5xl"    // Font size for the header
  textAlign="center" // Center text alignment
  fontFamily={"'Lilita One', cursive"}
  zIndex="1000"     // Ensure the header stays on top of other content
  borderRadius="30px"    // Added border radius to round the corners
 
>
  
  DocEase~ Chat with Your PDF
</Box>

{/* Chat input form fixed at the bottom */}
{isChatFormVisible && (
  <form
    onSubmit={handleSubmitChat}
    action=""
    style={{
      position: "absolute", // Make the form stick to the bottom
      bottom: "20px", // Set distance from the bottom
      width: "100%",
      padding: "20px",
      display: "flex", // Use flex to align items horizontally
      alignItems: "center" // Center align items vertically
    }}
  >
     {/* Microphone Button */}
     <Button
      color="white"
      bg="#0F2C59"
      height="50px"
      width="50px"
      borderRadius="full"
      display="flex"
      justifyContent="center"
      alignItems="center"
      marginLeft={"170px"}
      // marginRight="10px" // Add some space between the mic and input
      onClick={handleVoiceInput} // Function to handle voice input
    >
      <FaMicrophone size={24} />
    </Button>
    <Input
      border="1px solid black"
      marginLeft="12px"
      h="40px"
      w="600px"
      fontSize={"xl"}
      type="text"
      value={userMessage}
      onChange={(e) => setUserMessage(e.target.value)}
      textAlign="left"
      placeholder="Message DocEASE"
      fontWeight={"semibold"}
      borderRadius="20px" 
    />
    
    <Button
      _hover={{ bg: "#0F2C59" }}
      color="white"
      bg="#0F2C59"
      type="submit"
      height="50px"
      width="50px" // Adjust width to make it circular
      borderRadius="full" // Make it circular
      display="flex" // Use flex to center the arrow icon
      justifyContent="center" // Center the icon horizontally
      alignItems="center" // Center the icon vertically
      marginLeft="10px" // Add some space between the input and button
      // padding="0" // Remove default padding
    >
      <ArrowUpIcon boxSize={6} /> {/* Adjust boxSize for icon size */}
    </Button>
      {/* Sound Button to read the LLM response */}
      <Button
                _hover={{ bg: "#0F2C59" }}
                color="white"
                bg="#0F2C59"
                height="50px"
                width="50px"
                borderRadius="full"
                display="flex"
                justifyContent="center"
                alignItems="center"
                marginLeft="10px"
                onClick={() => handleTextToSpeech(chatResult[chatResult.length - 1]?.content)}
                disabled={!chatResult.length} // Disable if there's no chat result yet
              >
                <FaVolumeUp size={24} />
      </Button>
  </form>
)}


{/* // Chat messages container */}
<Box
  h="80%"
  overflowY="scroll"
  display="flex"
  flexDirection="column" // Change this to column
  paddingBottom="100px" // Padding to avoid overlap with the input box
>
  {chatResult.map((message, index) => (
    <div
      key={index}
      style={{
        width: "100%",
        padding: "10px 30px",
        display: "flex",
        justifyContent: message.role === "user" ? "flex-end" : "flex-start", // Align based on the message role
      }}
    >
      <div
        className={`message-container ${message.role === "user" ? "user-message" : "bot-message"}`}
        style={{
          maxWidth: "70%", // Adjust width as needed
          backgroundColor: message.role === "user" ? "#0F2C59" : "#0F2C59", // Different colors for user and bot
          color: "white",
          padding: "10px",
          borderRadius: "30px",
          marginBottom: "10px", // Add some space between messages
          boxShadow: "rgba(6, 24, 44, 0.4) 0px 0px 0px 2px, rgba(6, 24, 44, 0.65) 0px 4px 6px -1px, rgba(255, 255, 255, 0.08) 0px 1px 0px inset",
        }}
      >
        <strong>{message.role === "user" ? "You" : "DocEase"}:</strong>{" "}
        {message.content}
      </div>
    </div>
  ))}

  {/* Loader */}
  <Box>
    {isLoading && (
      <div className="loader" style={{ textAlign: "center" }}>
        <img
          style={{ mixBlendMode: "multiply", width: "15%", position: "relative", left: "20px" }}
          src={loading}
          alt=""
        />
      </div>
    )}
  </Box>
</Box>


    </Box>
  </Flex>
</Flex>

  );
};

const fill = keyframes`
  
  from {
    top : 200px;
    transform : translateX(-50%) rotate(0deg);
  }

  to {
    top : -50px;
    transform : translateX(-50%) rotate(360deg);
  }

`;

const LoadingStyle = styled.div`

width : 200px;
height : 200px;
border-radius : 30%;
margin : auto;
position : relative;
overflow : hidden;
background-color : #DAC0A3;
z-index : 2;

&:before{
  content : "";
  position : absolute;
  width : 400px;
  height : 400px;
  background-color : #00acee;
  left : 50%;
  transform : translateX(-50%);
  top : 200px;
  border-radius : 40%;
  z-index : -2;
  animation: ${(props) =>
    props.isAnimationActive
      ? css`
          ${fill} 7s ease-in-out
        `
      : "none"};
  }
}

`;