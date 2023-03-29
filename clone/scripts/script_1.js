// El load para que se cargue antes que la pagina
window.addEventListener("load", () => {
  // Objetos provisorio con los datos del usuario y validacion
  /* -------------------------- estado por defecto ------------------------- */
  
  const user = {
    user_name: "",
    email: "",
    password: "", // aca habria que generar un token
    // se podrian incluir mas datos
  };
  // ponemos en true solo cuando estén correctos
  const estadoErroresOK = {
    user_name: false,
    email: false,
    password: false,
    terminos: false, 
  };

  /* ---------------------------------- nodos --------------------------------- */

  // capturamos todos los elementos que necesitamos
  const formulario = document.querySelector(".form")

  const inputEmail = document.querySelector("#email");
  const inputPassword = document.querySelector("#password");
  const inputUser_name = document.querySelector("#nombreUsuario");
  const inputTerminos = document.querySelector("#terminos");
  

  const emailError = document.querySelector("#emailError");
  const passwordError = document.querySelector("#passwordError");
  const userError = document.querySelector("#nombreError");
  const terminosError = document.querySelector("#terminosError");

  /* -------------------------------------------------------------------------- */
  /*                   [1] FUNCION: mostrar errores al usuario                  */
  /* -------------------------------------------------------------------------- */
  function mostrarErrores() {
    // por cada small mostramos u ocultamos el error
    estadoErroresOK.email
      ? emailError.classList.remove("visible")
      : emailError.classList.add("visible");

    estadoErroresOK.password
      ? passwordError.classList.remove("visible")
      : passwordError.classList.add("visible");

    estadoErroresOK.nombreUsuario
      ? userError.classList.remove("visible")
      : userError.classList.add("visible");

    estadoErroresOK.terminos
      ? terminosError.classList.remove("visible")
      : terminosError.classList.add("visible");
  }

  /* -------------------------------------------------------------------------- */
  /*               [2] FUNCION: actulizamos los estados de la app               */
  /* -------------------------------------------------------------------------- */

  // 👇 por cada cambio en el formulario actualizamos
  formulario.addEventListener("change", function () {
    // 👇 actualizo el estado de la pantalla con los datos
    user.email = inputEmail.value;
    user.password = inputPassword.value;
    user.user_name = inputUser_name.value;
    user.terminos = inputTerminos.checked;

    // 👇 actualizo el estado del error segun el estado del usuario
    estadoErroresOK.email = validarEmail(user.email);
    estadoErroresOK.password = validarPassword(user.password);
    estadoErroresOK.user_name = validarUsername(user.user_name);
    estadoErroresOK.terminos = validarTerminos(user.terminos);

    // finalmente muestro los errores presentes
    mostrarErrores();
  });

  /* -------------------------------------------------------------------------- */
  /*                        [3] FUNCIONES: validar campos                       */
  /* -------------------------------------------------------------------------- */
  function validarEmail(email) {
    let resultado = false;

    // // EJEMPLO VALIDACIÓN A MANO 👇
    // if (email.includes('@') && email.includes('.') && !email.includes(' ') && email.length > 5) {
    //     resultado = true;
    // }

    // EJEMPLO CON EXPRESION REGULAR 👇
    let regex = new RegExp("[a-z0-9]+@[a-z]+.[a-z]{2,3}");

    if (regex.test(email)) {
      resultado = true;
    }

    return resultado;
  }

  function validarPassword(password) {
    let resultado = false;

    // si pasa las pruebas lo damos por válido 👇
    if (password.length > 5 && !password.includes(" ")) {
      resultado = true;
    }

    return resultado;
  }

  function validarUsername(nombreUsuario) {
    let resultado = false;
    let regex = new RegExp("/^[a-zA-Z0-9_]+$/");
    if
    (regex.test(nombreUsuario)){
        resultado = true
    }
    return resultado
  }
  // Verificar que tenga entre 4 y 20 caracteres
  // if (nombreUsuario.length < 4 || nombreUsuario.length > 20) {

  //     return false;
  //     }
  // // Verificar que sólo tenga letras, números y guiones bajos
  //     let expresionRegular = new RegExp("/^[a-zA-Z0-9_]+$/");
  //     if (!expresionRegular.test(nombreUsuario)) {

  //     return false;
  //     }
  //     return true;
  //   }
  // ACA HAY QUE VALIDAR SI EL USER_NAME ESTA EN USO TAMBIEN

  function validarTerminos(verificacion) {
    let resultado = false;

    // si pasa las pruebas lo damos por válido 👇
    if (verificacion) {
      resultado = true;
    }

    return resultado;
  }

  /* -------------------------------------------------------------------------- */
  /*                      [4] FUNCION: escuchamos el submit                     */
  /* -------------------------------------------------------------------------- */

  // en el evento submit nos remitimos a chequear nuestro estado de errores
  formulario.addEventListener("submit", function (evento) {
    // prevenimos el default para manejar nososotro el comportamiento
    evento.preventDefault();

    console.log(user);
    console.log(estadoErroresOK);

    if (
      estadoErroresOK.email &&
      estadoErroresOK.password &&
      estadoErroresOK.user_name &&
      estadoErroresOK.terminos
    ) {
      // alert("Pasó todas las validaciones!");
      // ☝ luego reemplazar esto por la funcion de éxito
      navegarPaginaExito();
    }
  });
  // Para ir redireccionando
  function navegarPaginaExito() {
    const formulario = document.querySelector("form");
    const botonSubmit = formulario.querySelector(".boton");

    botonSubmit.disabled = true;
    botonSubmit.innerHTML = "Loading...";
    localStorage.setItem("nuevoDato", JSON.stringify(user));
    setTimeout(() => {
      window.location.replace("/templates/usuario");
    }, 3000);
  }
});
