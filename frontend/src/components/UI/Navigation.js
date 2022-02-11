import React from "react";
import ButtonNav from "./ButtonNav/ButtonNav";

const Navigation = () => {
  return (
    <div className="mx-auto flex max-w-7xl items-center justify-center">
      <nav className="hidden items-center space-x-2 text-md font-medium text-gray-800 md:flex">
        <ButtonNav activeClassName="active" to="/me">
          Perfil
        </ButtonNav>
      </nav>
    </div>
  );
};

export default Navigation;
