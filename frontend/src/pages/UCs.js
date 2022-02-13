import React, { useState, useContext, useEffect } from "react";
import { useQuery } from "react-query";
import AuthContext from "../store/auth-context";
import ucService from "../_services/ucServices";

const UCs = () => {
  const authCtx = useContext(AuthContext);
  const [ucs, setUcs] = useState(null);

  const { isLoading, data } = useQuery(["ucs", authCtx], () =>
    ucService.fetchUCs(authCtx)
  );

  useEffect(() => {
    setUcs(data);
    console.log("eff");
  }, [data, isLoading]);

  return (
    <section className="mx-auto flex flex-col max-w-7xl p-4 mt-4">
      <p className="text-2xl text-left border-b-8 border-red-400 mb-8">
        <span className=" translate-x-10">A suas disciplinas</span>
      </p>
      {isLoading ? (
        <p>Loading</p>
      ) : (
        <div className="flex flex-col items-center">
          {data.map((uc) => (
            <div className="flex w-full p-2 text-left rounded-md md:w-1/2 border-2 shadow-md">
              <p className=" text-xl">{uc.nome_uc}</p>
            </div>
          ))}{" "}
        </div>
      )}
    </section>
  );
};

export default UCs;
