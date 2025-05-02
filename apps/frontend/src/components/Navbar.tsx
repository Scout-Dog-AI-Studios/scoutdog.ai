"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Menu, X, LogIn, LogOut } from "lucide-react";
import Link from "next/link";
import { useAuth0 } from "@auth0/auth0-react";

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { isAuthenticated, loginWithRedirect, logout, isLoading } = useAuth0();

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 10) {
        setIsScrolled(true);
      } else {
        setIsScrolled(false);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 w-full z-50 transition-all duration-300 ${
        isScrolled ? "bg-white shadow-md py-2" : "bg-transparent py-4"
      }`}
    >
      <div className="container mx-auto px-4 md:px-6 flex justify-between items-center">
        <Link href="/" className="flex items-center">
          <span className="text-xl md:text-2xl font-bold text-scoutdog-black">
            Scout Dog
          </span>
          <span className="text-xl md:text-2xl font-bold text-scoutdog-blue">
            &nbsp;AI&nbsp;
          </span>
          <span className="text-xl md:text-2xl font-bold text-scoutdog-black">
            Studios
          </span>
        </Link>

        {/* Desktop Nav Items */}
        <div className="hidden md:flex items-center space-x-6">
          <Link
            href="/projects"
            className="font-medium text-gray-800 hover:text-scoutdog-blue transition-colors"
          >
            Projects
          </Link>
          <Link
            href="/#contact"
            className="font-medium text-gray-800 hover:text-scoutdog-blue transition-colors"
          >
            Contact
          </Link>
          {isLoading ? (
            <Button variant="outline" disabled>
              Loading...
            </Button>
          ) : isAuthenticated ? (
            <Button
              variant="outline"
              className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white transition-colors"
              onClick={() =>
                logout({ logoutParams: { returnTo: window.location.origin } })
              }
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          ) : (
            <Button
              variant="outline"
              className="border-scoutdog-blue text-scoutdog-blue hover:bg-scoutdog-blue hover:text-white transition-colors"
              onClick={() => loginWithRedirect()}
            >
              <LogIn className="w-4 h-4 mr-2" />
              Login
            </Button>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="md:hidden text-gray-800"
          aria-label="Toggle Menu"
        >
          {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white shadow-lg py-4 px-6 absolute w-full">
          <div className="flex flex-col space-y-4">
            <Link
              href="/projects"
              className="font-medium text-gray-800 hover:text-scoutdog-blue transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Projects
            </Link>
            <Link
              href="/#contact"
              className="font-medium text-gray-800 hover:text-scoutdog-blue transition-colors"
              onClick={() => setIsMobileMenuOpen(false)}
            >
              Contact
            </Link>
            {isLoading ? (
              <Button variant="outline" disabled className="w-full">
                Loading...
              </Button>
            ) : isAuthenticated ? (
              <Button
                variant="outline"
                className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white transition-colors w-full"
                onClick={() =>
                  logout({ logoutParams: { returnTo: window.location.origin } })
                }
              >
                <LogOut className="w-4 h-4 mr-2" />
                Logout
              </Button>
            ) : (
              <Button
                variant="outline"
                className="border-scoutdog-blue text-scoutdog-blue hover:bg-scoutdog-blue hover:text-white transition-colors w-full"
                onClick={() => loginWithRedirect()}
              >
                <LogIn className="w-4 h-4 mr-2" />
                Login
              </Button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
