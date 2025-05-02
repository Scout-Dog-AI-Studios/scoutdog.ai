import { Button } from "@/components/ui/button";
import { ExternalLink } from "lucide-react";
import Link from "next/link";

const projects = [
  {
    title: "AI Content Assistant",
    description:
      "An intelligent writing assistant that helps create and optimize content for various platforms.",
    tags: ["AI", "NLP", "Content"],
    color: "from-blue-400 to-blue-600",
    slug: "ai-content-assistant",
  },
  {
    title: "Data Visualization Suite",
    description:
      "Turn complex datasets into beautiful, interactive visualizations that tell compelling stories.",
    tags: ["Data", "Analytics", "Charts"],
    color: "from-green-400 to-green-600",
    slug: "data-visualization-suite",
  },
  {
    title: "Process Automation Tool",
    description:
      "Streamline workflows and automate repetitive tasks to boost productivity across teams.",
    tags: ["Automation", "Workflow", "Productivity"],
    color: "from-purple-400 to-purple-600",
    slug: "process-automation-tool",
  },
];

const Projects = () => {
  return (
    <section id="projects" className="py-20">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">Our Projects</h2>
          <p className="text-lg text-gray-600">
            Explore some of our innovative applications built with cutting-edge
            AI technology.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {projects.map((project, index) => (
            <div
              key={index}
              className="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 animate-fade-in flex flex-col"
              style={{ animationDelay: `${0.2 * index}s` }}
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
                <Link href={`/projects/${project.slug}`}>
                  <Button className="w-full bg-gray-100 text-gray-800 hover:bg-gray-200">
                    Learn More <ExternalLink className="h-4 w-4 ml-2" />
                  </Button>
                </Link>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-12">
          <Link href="/projects">
            <Button
              variant="outline"
              className="border-scoutdog-blue text-scoutdog-blue hover:bg-scoutdog-blue hover:text-white"
            >
              View All Projects
            </Button>
          </Link>
        </div>
      </div>
    </section>
  );
};

export default Projects;
