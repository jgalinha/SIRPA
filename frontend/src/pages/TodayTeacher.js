import React, { useContext, useState } from "react";
import { useQuery } from "react-query";
import AuthContext from "../store/auth-context";
import crudService from "../_services/crudServices";
import { toast, Toaster } from "react-hot-toast";
import ClassSchedule from "../components/teachers/ClassSchedule";

const TodayStudent = () => {
  const authCtx = useContext(AuthContext);
  const [schedule, setSchedule] = useState({
    id_docente: "",
    ucs: [],
  });
  const [erro, setErro] = useState({
    code: null,
    msg: null,
    error_detail: null,
  });

  const onSuccess = (data) => {
    const new_schedule = {
      id_docente: data.id_docente,
      ucs: [],
    };
    if (data.aulas !== null) {
      data.aulas.forEach((aula) => {
        new_schedule.ucs.push({
          ic_uc: aula.uc.id_uc,
          id_aula: aula.id_aula,
          resumo: aula.resumo,
          sala: aula.sala,
          presencas: aula.presencas.length,
          hora_inicio: aula.periodo.hora_inicio,
          hora_fim: aula.periodo.hora_fim,
          data: aula.data,
          nome_uc: aula.uc.nome_uc,
          nome_curso: aula.uc.curso.nome_curso,
        });
      });
    }
    setSchedule(new_schedule);
  };

  const onError = (error) => {
    const detail = error.response.data.detail.error;
    setErro({ ...detail });
    toast.error("Erro ao carregar as disciplinas");
    toast.error(erro.msg);
  };

  const { isLoading, isError } = useQuery(
    ["today", authCtx],
    () => {
      return crudService.fetchAPI(authCtx, "/teacher/today");
    },
    { onSuccess, onError }
  );

  return (
    <section className="mx-auto flex flex-col max-w-7xl p-4 mt-4">
      <div>
        <Toaster />
      </div>
      <p className="text-2xl text-left border-b-8 border-red-400 mb-8">
        <span className="">O teu dia!</span>
      </p>
      <div className="flex flex-col items-center text-2xl font-bold">
        {isLoading && <p>🔎 Procurando as tuas aulas para hoje!</p>}
        {!isLoading && !isError && schedule.ucs !== null && (
          <ClassSchedule schedule={schedule} />
        )}
        {!isLoading && !isError && schedule.ucs.length === 0 && (
          <p className=" text-2xl font-bold">
            Não tens aulas hoje, aproveita! 🎉
          </p>
        )}
        {isError && (
          <div className=" text-center text-2xl font-bold">
            <p>❌ Erro ao carregar as disciplinas! </p>
            <p>{erro.msg}</p>
          </div>
        )}
      </div>
    </section>
  );
};

export default TodayStudent;
