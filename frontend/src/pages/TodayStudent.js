import React, { useContext, useState } from "react";
import { useQuery } from "react-query";
import AuthContext from "../store/auth-context";
import crudService from "../_services/crudServices";
import { toast, Toaster } from "react-hot-toast";
import ClassSchedule from "../components/students/ClassSchedule";

const TodayStudent = () => {
  const authCtx = useContext(AuthContext);
  const [schedule, setSchedule] = useState({
    id_aluno: "",
    ucs: [],
  });
  const [erro, setErro] = useState({
    code: null,
    msg: null,
    error_detail: null,
  });

  const onSuccess = (data) => {
    const new_schedule = {
      id_aluno: data.id_aluno,
      ucs: [],
    };
    if (data.inscricoes_ucs !== null) {
      data.inscricoes_ucs.forEach((uc) => {
        if (uc.uc !== null) {
          uc.uc.periodos.forEach((periodo) => {
            new_schedule.ucs.push({
              id_uc: uc.id_uc,
              id_aula: periodo.aulas[0].id_aula,
              id_docent: periodo.aulas[0].id_docente,
              resumo: periodo.aulas[0].resumo,
              sala: periodo.aulas[0].sala,
              hora_inicio: periodo.hora_inicio,
              hora_fim: periodo.hora_fim,
              data: periodo.aulas[0].data,
              nome_uc: uc.uc.nome_uc,
            });
          });
        }
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
      return crudService.fetchAPI(authCtx, "/student/today");
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
