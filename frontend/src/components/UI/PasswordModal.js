import { Dialog, Transition } from "@headlessui/react";
import { Fragment, useState, useRef, useContext } from "react";
import Button from "./Button/Button";
import { QRCode } from "react-qr-svg";
import AuthContext from "../../store/auth-context";
import crudService from "../../_services/crudServices";

export default function PasswordModal(props) {
  const authCtx = useContext(AuthContext);
  const passwordInput = useRef();
  const [showQRCode, setShowQRCode] = useState(false);
  const [presenca, setPresenca] = useState({
    id_aula: "",
    password: "",
  });
  const [qrcode, setQrcode] = useState("");
  function closeModal() {
    setShowQRCode(false);
    setQrcode("");
    props.onClose();
  }

  const requestQRCode = (data) => {
    const request = crudService.postAPI(
      authCtx,
      "/class/qrcode",
      { ...data },
      setQrcode
    );
  };

  const submitHandler = () => {
    requestQRCode({
      id_aula: props.idAula,
      password: passwordInput.current.value,
    });
    setShowQRCode(true);
  };

  return (
    <>
      <Transition appear show={props.open} as={Fragment}>
        <Dialog
          as="div"
          className="fixed inset-0 z-10 overflow-y-auto"
          onClose={closeModal}
          initialFocus={passwordInput}
        >
          <div className="min-h-screen px-4 text-center">
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0"
              enterTo="opacity-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100"
              leaveTo="opacity-0"
            >
              <Dialog.Overlay className="fixed inset-0" />
            </Transition.Child>

            {/* This element is to trick the browser into centering the modal contents. */}
            <span
              className="inline-block h-screen align-middle"
              aria-hidden="true"
            >
              &#8203;
            </span>
            <Transition.Child
              as={Fragment}
              enter="ease-out duration-300"
              enterFrom="opacity-0 scale-95"
              enterTo="opacity-100 scale-100"
              leave="ease-in duration-200"
              leaveFrom="opacity-100 scale-100"
              leaveTo="opacity-0 scale-95"
            >
              <div className="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle transition-all transform bg-white shadow-xl rounded-2xl">
                <Dialog.Title
                  as="h3"
                  className="text-lg font-medium leading-6 text-gray-900"
                >
                  {!showQRCode && <span>Introduz a tua password!</span>}
                  {showQRCode && <span>Mostra o teu QRCode ao professor!</span>}
                </Dialog.Title>
                <div className="mt-2">
                  {!showQRCode && (
                    <>
                      <label className="font-semibold text-sm text-gray-600 pb-1 block">
                        Password
                      </label>
                      <input
                        type="password"
                        className="border rounded-lg px-3 py-2 mt-1 mb-5 text-sm w-full"
                        ref={passwordInput}
                      />
                      <Button type="button" onClick={submitHandler}>
                        <span className="inline-block mr-2">Gerar QRCode</span>
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          className="w-4 h-4 inline-block"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="2"
                            d="M17 8l4 4m0 0l-4 4m4-4H3"
                          />
                        </svg>
                      </Button>{" "}
                    </>
                  )}
                  {showQRCode && <QRCode value={JSON.stringify(qrcode)} />}
                </div>

                <div className="mt-4">
                  <button
                    type="button"
                    className="inline-flex justify-center px-4 py-2 text-sm font-medium text-red-900 bg-red-100 border border-transparent rounded-md hover:bg-red-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-red-500"
                    onClick={closeModal}
                  >
                    Fechar
                  </button>
                </div>
              </div>
            </Transition.Child>
          </div>
        </Dialog>
      </Transition>
    </>
  );
}
