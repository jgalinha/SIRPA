import React from "react";
import ButtonNav from "./ButtonNav/ButtonNav";
import { CalendarIcon, BookOpenIcon } from "@heroicons/react/outline";

const Navigation = () => {
  return (
    <nav className="mx-auto flex max-w-7xl items-center justify-center">
      <div className="hidden items-center space-x-0 text-md font-medium text-gray-800 md:flex">
        <ButtonNav activeClassName="active" to="/today">
          <CalendarIcon className="mr-3 h-5 w-5" aria-hidden="true" />
          Hoje!
        </ButtonNav>
        <ButtonNav activeClassName="active" to="/ucs">
          <BookOpenIcon className="mr-3 h-5 w-5" aria-hidden="true" />
          Disciplinas
        </ButtonNav>
      </div>
    </nav>
  );
};

export default Navigation;
