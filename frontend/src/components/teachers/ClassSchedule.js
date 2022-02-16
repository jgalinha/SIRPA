import React, { useState, useEffect, useContext } from "react";
import moment from "moment";
import "moment/locale/pt";
import AuthContext from "../../store/auth-context";
import { CameraIcon } from "@heroicons/react/outline";
import crudService from "../../_services/crudServices";
import Html5QrcodeReader from "../UI/Html5QrcodeReader";

const ClassSchedule = (props) => {
  moment.locale("pt");
  const authCtx = useContext(AuthContext);
  const [ucs, setUcs] = useState([
    {
      id_uc: "",
      id_aula: "",
      id_docente: "",
      resumo: "",
      sala: "",
      hora_inicio: "",
      hora_fim: "",
      data: "",
      nome_uc: "",
      nome_curso: "",
    },
  ]);
  const [showReader, setShowReader] = useState(false);

  useEffect(() => {
    // TODO: order by hour
    setUcs(
      props.schedule.ucs.sort((a, b) => {
        return a.data - b.data;
      })
    );
  }, [props]);

  const handleQRCodeScan = (decodedText, decodedResult) => {
    const obj = JSON.parse(decodedText.text);
    console.log(obj);
  };

  return (
    <ul className="flex flex-col w-full items-center">
      {ucs.map((uc, index) => {
        return (
          <div
            key={index}
            className=" bg-slate-100 rounded-2xl w-full md:w-3/5 p-4 shadow list-none mb-4"
          >
            <span className="text-gray-900 uppercase font-medium tracking-widest">
              📆 {moment(uc.data).format("MMMM D")}
            </span>
            <div className="flex sm:flex-row mb-2 mt-2">
              <div className="w-2/12">
                <span className="text-sm text-gray-600 block">
                  {moment(uc.hora_inicio, "HH:mm:ss").format("HH:mm")}
                </span>
                <span className="text-sm text-gray-600 block">
                  {moment(uc.hora_fim, "HH:mm:ss").format("HH:mm")}
                </span>
              </div>
              <div className="w-1/12">
                <span
                  className={` invisible md:visible h-2 w-2 bg-blue-400 rounded-full block mt-2`}
                ></span>
              </div>
              <div className="w-9/12">
                <span className="text-sm font-semibold block">
                  {uc.nome_uc}{" "}
                  <span className=" font-light">({uc.nome_curso})</span>
                </span>
                <span className="text-sm block font-thin">{uc.resumo}</span>
                <span className="text-sm block font-normal">
                  Sala {uc.sala}
                </span>
              </div>
              <div className="w-1/12 mr-2">
                <CameraIcon
                  onClick={() => {
                    setShowReader(!showReader);
                  }}
                  className="w-12 h-12 hover:stroke-red-500 hover:cursor-pointer"
                />
              </div>
            </div>
            {showReader && (
              <Html5QrcodeReader
                fps={24}
                qrbox={250}
                disableFlip={false}
                qrCodeSuccessCallback={handleQRCodeScan}
              />
            )}
          </div>
        );
      })}
    </ul>
  );
};

export default ClassSchedule;
