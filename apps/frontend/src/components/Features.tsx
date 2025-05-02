import { Cpu, Code, LineChart, Bot, Zap, BoltIcon } from "lucide-react";

const features = [
  {
    icon: <Cpu className="h-10 w-10 text-scoutdog-blue" />,
    title: "AI Integration",
    description:
      "Seamlessly integrate cutting-edge AI technologies into efficient web applications that solve real-world problems.",
  },
  {
    icon: <Code className="h-10 w-10 text-scoutdog-blue" />,
    title: "Full-Stack Development",
    description:
      "End-to-end development with Python backends and modern NextJS/Tailwind frontends for optimal performance.",
  },
  {
    icon: <LineChart className="h-10 w-10 text-scoutdog-blue" />,
    title: "Data Analytics",
    description:
      "Transform raw data into actionable insights with intelligent analytics powered by machine learning.",
  },
  {
    icon: <Bot className="h-10 w-10 text-scoutdog-blue" />,
    title: "Automation Tools",
    description:
      "Build custom automation solutions that save time and reduce errors in your business processes.",
  },
  {
    icon: <Zap className="h-10 w-10 text-scoutdog-blue" />,
    title: "Rapid Prototyping",
    description:
      "Quickly test and iterate on ideas with our efficient prototyping methodology and toolchain.",
  },
  {
    icon: <BoltIcon className="h-10 w-10 text-scoutdog-blue" />,
    title: "Performance Optimization",
    description:
      "Ensure your applications run at peak performance with our optimization techniques and best practices.",
  },
];

const Features = () => {
  return (
    <section id="features" className="py-20 bg-scoutdog-gray">
      <div className="container mx-auto px-4 md:px-6">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Powered by Intelligence
          </h2>
          <p className="text-lg text-gray-600">
            Our suite of tools and services leverage the latest in artificial
            intelligence to create applications that are both powerful and
            intuitive.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <div
              key={index}
              className="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow duration-300 animate-slide-up"
              style={{ animationDelay: `${0.1 * index}s` }}
            >
              <div className="mb-4 p-2 inline-block bg-blue-50 rounded-lg">
                {feature.icon}
              </div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
