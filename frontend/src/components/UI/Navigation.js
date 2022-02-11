import React from "react";
import ButtonNav from "./ButtonNav/ButtonNav";
import { CalendarIcon } from "@heroicons/react/outline";

const Navigation = () => {
  return (
    <div className="mx-auto flex max-w-7xl items-center justify-center">
      <nav className="hidden items-center space-x-2 text-md font-medium text-gray-800 md:flex">
        <ButtonNav activeClassName="active" to="/today">
          <CalendarIcon className="mr-3 h-5 w-5" aria-hidden="true" />
          Hoje!
        </ButtonNav>
      </nav>
    </div>
  );
};

export default Navigation;
