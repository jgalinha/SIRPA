import React from "react";
import ButtonNav from "./ButtonNav/ButtonNav";

const Navigation = () => {
  return (
    <div className="mx-auto flex max-w-7xl items-center justify-center p-2">
      <nav className="hidden items-center space-x-2 text-md font-medium text-gray-800 md:flex">
        <ButtonNav to="/me">Perfil</ButtonNav>
      </nav>
    </div>
  );
};

export default Navigation;
