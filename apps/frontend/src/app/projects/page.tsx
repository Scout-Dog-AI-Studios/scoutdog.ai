import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";

const projects = [
  {
    title: "AI Content Assistant",
    description:
      "An intelligent writing assistant that helps create and optimize content for various platforms.",
    tags: ["AI", "NLP", "Content"],
    color: "from-blue-400 to-blue-600",
  },
  {
    title: "Data Visualization Suite",
    description:
      "Turn complex datasets into beautiful, interactive visualizations that tell compelling stories.",
    tags: ["Data", "Analytics", "Charts"],
    color: "from-green-400 to-green-600",
  },
  {
    title: "Process Automation Tool",
    description:
      "Streamline workflows and automate repetitive tasks to boost productivity across teams.",
    tags: ["Automation", "Workflow", "Productivity"],
    color: "from-purple-400 to-purple-600",
  },
  {
    title: "Smart Document Scanner",
    description:
      "Extract and process information from documents using AI-powered OCR technology.",
    tags: ["OCR", "AI", "Documents"],
    color: "from-red-400 to-red-600",
  },
  {
    title: "Customer Insights Platform",
    description:
      "Analyze customer behavior and feedback to drive data-informed business decisions.",
    tags: ["Analytics", "Customer", "Insights"],
    color: "from-amber-400 to-amber-600",
  },
  {
    title: "Interactive Learning System",
    description:
      "Personalized learning experiences that adapt to individual student progress and needs.",
    tags: ["Education", "Adaptive", "Learning"],
    color: "from-teal-400 to-teal-600",
  },
];

export default function ProjectsPage() {
  return (
    <div className="pt-28 pb-20">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h1 className="text-3xl md:text-5xl font-bold mb-6">Our Projects</h1>
          <p className="text-lg text-gray-600">
            Explore our portfolio of innovative applications built with
            cutting-edge AI technology to solve real-world challenges.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <div
              key={index}
              className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 animate-fade-in flex flex-col"
              style={{ animationDelay: `${0.1 * (index + 1)}s` }}
            >
              <div className={`h-3 bg-gradient-to-r ${project.color}`}></div>
              <div className="p-6 flex-grow">
                <h3 className="text-xl font-semibold mb-3">{project.title}</h3>
                <p className="text-gray-600 mb-4">{project.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.tags.map((tag) => (
                    <span
                      key={tag}
                      className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
              <div className="px-6 pb-6">
                <Button className="w-full bg-gray-100 text-gray-800 hover:bg-gray-200">
                  View Details <ExternalLink className="h-4 w-4 ml-2" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
