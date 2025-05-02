import { Github, Twitter, Linkedin, Mail } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-2 space-y-4">
            <div className="flex items-center">
              <Image
                src="/scoutdog-logo.png"
                alt="Scout Dog AI Studios"
                width={48}
                height={48}
                className="bg-white p-1 rounded"
              />
            </div>
            <p className="text-gray-400 mt-4 max-w-md">
              Scout Dog AI Studio creates innovative web applications powered by
              artificial intelligence. We focus on building small but impactful
              tools that solve real problems.
            </p>
            <div className="flex space-x-4 mt-6">
              <a
                href="https://github.com/scoutdog-ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-scoutdog-blue transition-colors"
              >
                <Github className="h-5 w-5" />
              </a>
              <a
                href="https://twitter.com/scoutdog_ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-scoutdog-blue transition-colors"
              >
                <Twitter className="h-5 w-5" />
              </a>
              <a
                href="https://linkedin.com/company/scoutdog-ai"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-scoutdog-blue transition-colors"
              >
                <Linkedin className="h-5 w-5" />
              </a>
              <a
                href="mailto:contact@scoutdog.ai"
                className="text-gray-400 hover:text-scoutdog-blue transition-colors"
              >
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/#features"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Features
                </Link>
              </li>
              <li>
                <Link
                  href="/#projects"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Projects
                </Link>
              </li>
              <li>
                <Link
                  href="/#contact"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-lg mb-4">Resources</h3>
            <ul className="space-y-2">
              <li>
                <Link
                  href="/blog"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Blog
                </Link>
              </li>
              <li>
                <Link
                  href="/docs"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Documentation
                </Link>
              </li>
              <li>
                <Link
                  href="/privacy"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link
                  href="/terms"
                  className="text-gray-400 hover:text-scoutdog-blue transition-colors"
                >
                  Terms of Service
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-12 pt-8">
          <div className="text-center text-gray-500 text-sm">
            © {year} Scout Dog AI Studio. All rights reserved.
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
