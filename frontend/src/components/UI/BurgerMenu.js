import React from "react";
import { Menu, Transition } from "@headlessui/react";
import { MenuIcon, CalendarIcon } from "@heroicons/react/outline";
import { Link } from "react-router-dom";

const BurgerMenu = () => {
  return (
    <>
      <Menu as="div" className="relative">
        {({ open }) => (
          <>
            <Menu.Button>
              <MenuIcon className="flex appearance-none mt-1 md:hidden w-12 h-12" />
            </Menu.Button>
            <Transition
              show={open}
              enter="transform transition duration-100 ease-in"
              enterFrom="opacity-0 scale-05"
              enterTo="opacity-100 scale-100"
              leave="transform transition duration-75 ease-out"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <Menu.Items
                className="origin-top-right absolute right-0 mt-2 w-72 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none"
                static
              >
                <Menu.Item>
                  {({ active }) => (
                    <Link
                      to="/today"
                      className={`flex items-center px-4 py-2 text-lg ${
                        active && "bg-red-700 rounded-md text-white"
                      }`}
                    >
                      <CalendarIcon
                        className="mr-3 h-5 w-5"
                        aria-hidden="true"
                      />
                      Hoje!
                    </Link>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Transition>
          </>
        )}
      </Menu>
    </>
  );
};

export default BurgerMenu;
