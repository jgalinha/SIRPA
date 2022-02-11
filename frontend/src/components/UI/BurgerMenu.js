import React from "react";
import { Menu, Transition } from "@headlessui/react";
import { MenuIcon, UserIcon } from "@heroicons/react/outline";
import { Link } from "react-router-dom";

const BurgerMenu = () => {
  return (
    <>
      <Menu as="div" className="relative">
        {({ open }) => (
          <>
            <Menu.Button>
              <MenuIcon className="flex appearance-none p-1 md:hidden w-10 h-10" />
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
                className="origin-top-left absolute left-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 divide-y divide-gray-100 focus:outline-none"
                static
              >
                <Menu.Item>
                  {({ active }) => (
                    <Link
                      to="/student"
                      className={`flex items-center px-4 py-2 text-lg ${
                        active && "bg-red-700 text-white"
                      }`}
                    >
                      <UserIcon className="mr-3 h-5 w-5" aria-hidden="true" />
                      Perfil
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
