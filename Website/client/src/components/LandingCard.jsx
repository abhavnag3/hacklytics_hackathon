import { Link } from "wouter";
import { Card, CardContent } from "@/components/ui/card";

export default function LandingCard({ icon, title, description, href }) {
  return (
    <Link href={href}>
      <Card className="cursor-pointer hover:shadow-lg transition-shadow duration-200">
        <CardContent className="p-6">
          <div className="flex flex-col items-start gap-4">
            <div className="bg-blue-100 p-3 rounded-lg">
              {icon}
            </div>
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-2">{title}</h2>
              <p className="text-gray-600">{description}</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
