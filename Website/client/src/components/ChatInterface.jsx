import { useState } from "react";
import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Send } from "lucide-react";

export default function ChatInterface() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [queryResponse, setQueryResponse] = useState([]);
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (message.trim()) {
      // In a real app, this would send to an API
      // For now, we'll just log to console as the Python script will handle it
      setMessages([...messages, message]);
      try {
        const response = await fetch('http://localhost:5001/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ message: message }),
        });
        const data = await response.json();
        
        console.log('Server response:', data);
        console.log('ACTUAL DATA: ', data.message)
        setQueryResponse(data.message)

      } catch (error) {
        console.error('Error sending message:', error);
      }
      console.log(message);
      setMessage("");
    }
  };

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
          
          <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
            
            {/* Display the query response */}
            {queryResponse && (
              <div className="mb-2 p-2 bg-white rounded shadow">
                {queryResponse}
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
