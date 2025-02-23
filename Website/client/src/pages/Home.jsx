import { Card } from "@/components/ui/card";
import LandingCard from "@/components/LandingCard";
import { CreditCard, Briefcase } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-blue-100">
      <h1 className="text-4xl font-bold text-gray-800 mb-12">
        How can we help you today?
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-4">
        <LandingCard
          icon={<CreditCard className="h-6 w-6 text-blue-500" />}
          title="Get a Credit Card"
          description="Find the perfect credit card tailored to your needs"
          href="/credit-chat"
        />
        <LandingCard
          icon={<Briefcase className="h-6 w-6 text-blue-500" />}
          title="Start a Business"
          description="Get guidance on starting your business journey"
          href="/business-chat"
        />
      </div>
    </div>
  );
}
