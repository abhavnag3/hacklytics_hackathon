import { useState } from "react";
import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Send, Loader } from "lucide-react";

export default function ChatInterfaceConsumer() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [queryResponse, setQueryResponse] = useState([]);
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim()) {
      setLoading(true);
      // In a real app, this would send to an API
      // For now, we'll just log to console as the Python script will handle it
      setMessages([...messages, message]);
      try {
        const response = await fetch('http://localhost:5001/chat_consumer', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: message }),
        });
        const data = await response.json();
        
        let cleanedAnswer = data.message;
        if (cleanedAnswer.includes("QUESTION:") && cleanedAnswer.includes("Answer:")) {
          // Assume the response is something like:
          // "QUESTION: <...>
          //  Answer: <clean answer>"
          // Split on "Answer:" and take the text after it.
          cleanedAnswer = cleanedAnswer.split("Answer:")[1].trim();
        }
        setConversation((prev) => [
          ...prev,
          { question: message, answer: cleanedAnswer },
        ]);
        
        console.log('Server response:', data);
        console.log('ACTUAL DATA: ', data.message)
        setQueryResponse(data.message)

      } catch (error) {
        console.error('Error sending message:', error);
      } finally {
        setLoading(false);
      }
      console.log(message);
      setMessage("");
    }
  };

  let questionPart = "";
  let answerPart = "";
  if (queryResponse) {
    const questionMarker = "QUESTION:";
    const answerMarker = "Answer:";
    const questionIndex = queryResponse.indexOf(questionMarker);
    const answerIndex = queryResponse.indexOf(answerMarker);
    if (questionIndex !== -1 && answerIndex !== -1) {
      questionPart = queryResponse
        .substring(questionIndex + questionMarker.length, answerIndex)
        .trim();
      answerPart = queryResponse
        .substring(answerIndex + answerMarker.length)
        .trim();
    } else {
      // Fallback if the markers are not found
      answerPart = queryResponse;
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-blue-100 p-4">
      <Card className="max-w-2xl mx-auto h-[calc(100vh-2rem)]">
        <CardContent className="p-4 h-full flex flex-col">
          <div className="flex items-center gap-2 mb-6">
            <Link href="/">
              <Button variant="ghost" size="sm" className="gap-2">
                <ArrowLeft className="h-4 w-4" />
                Back to Home
              </Button>
            </Link>
          </div>
          
          <div className="flex-1 relative overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
            {conversation.length > 0 &&
              conversation.map((conv, index) => (
                <div key={index} className="mb-4">
                  {/* Question block */}
                  <div className="mb-2 p-2 bg-white rounded-lg shadow">
                    <p className="font-bold">Question:</p>
                    <p>{conv.question}</p>
                  </div>
                  {/* Answer block with preserved newlines */}
                  <div
                    className="mb-2 p-2 bg-white rounded-lg shadow"
                    style={{ whiteSpace: "pre-line" }}
                  >
                    <p className="font-bold">Answer:</p>
                    <p>{conv.answer}</p>
                  </div>
                </div>
              ))}

            {loading && (
              <div className="absolute inset-0 flex justify-center items-center bg-gray-50 bg-opacity-75">
                <Loader className="h-6 w-6 animate-spin text-gray-500" />
              </div>
            )}
          </div>

          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1"
            />
            <Button type="submit">
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
