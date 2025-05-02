import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";
import Image from "next/image";

const Hero = () => {
  return (
    <section className="pt-28 pb-20 md:pt-36 md:pb-28 bg-gradient-to-b from-white to-scoutdog-gray/30">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div
            className="lg:col-span-7 space-y-6 animate-fade-in"
            style={{ animationDelay: "0.2s" }}
          >
            <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6 mb-6">
              <div>
                <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight">
                  Small Apps. Big Impact.
                  <br />
                  <span className="text-scoutdog-blue">AI-Powered</span>{" "}
                  Innovation.
                </h1>
              </div>
            </div>

            <p className="text-lg md:text-xl text-gray-600 max-w-2xl">
              Scout Dog AI Studio builds intelligent web applications that solve
              real problems. We combine the power of artificial intelligence
              with intuitive design to create tools that matter.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 pt-4">
              <Button className="bg-scoutdog-blue hover:bg-scoutdog-blue/90 text-white px-8 py-6">
                Get Started <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
              <Button
                variant="outline"
                className="border-gray-300 hover:bg-gray-50 px-8 py-6"
              >
                Learn More
              </Button>
            </div>
          </div>

          <div
            className="lg:col-span-5 flex items-center justify-center animate-fade-in"
            style={{ animationDelay: "0.4s" }}
          >
            <div className="relative w-full h-full max-h-[400px] flex items-center justify-center">
              <div className="absolute inset-0 bg-gradient-to-r from-scoutdog-blue/20 to-blue-400/20 rounded-full blur-xl opacity-70"></div>
              <div className="relative w-full h-full max-w-md">
                <Image
                  src="/scoutdog-logo.png"
                  alt="Scout Dog AI Studios Logo"
                  width={400}
                  height={400}
                  className="w-full h-full object-contain"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
