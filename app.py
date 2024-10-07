<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">

    <script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>

    <script src="https://js.pusher.com/8.2.0/pusher.min.js"></script>

    <title>App</title>
</head>
<body>
    <div class="container">
      <form id="frmTemperaturaHumedad" method="post">
          <input type="hidden" id="id" name="id">

          <div class="mb-1">
              <label for="temperatura">Temperatura</label>
              <input type="number" id="temperatura" name="temperatura" class="form-control">
          </div>
          <div class="mb-1">
              <label for="humedad">Humedad</label>
              <input type="number" id="humedad" name="humedad" class="form-control">
          </div>
          <div class="mb-1">
              <button id="guardar" name="guardar" class="btn btn-dark">Guardar</button>
              <button type="reset" id="cancelar" name="cancelar" class="btn btn-link">Cancelar</button>
          </div>
      </form>
      <table class="table table-sm">
        <thead>
          <tr>
            <th>Temperatura</th>
            <th>Humedad</th>
            <th>Fecha</th>
            <th>Hora</th>
            <th></th>
          </tr>
        </thead>
        <tbody id="tbodyTemperaturaHumedad"></tbody>
      </table>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <div class="app-float-button bg-body" style="z-index: 3; position: fixed; bottom: 5px; left: 5px; cursor: pointer;">
        <ul class="list-group list-group-horizontal">
            <li class="list-group-item" data-bs-theme-value="light">
                <i class="bi bi-sun-fill"></i>
            </li>
            <li class="list-group-item" data-bs-theme-value="dark">
                <i class="bi bi-moon-stars-fill"></i>
            </li>
            <li class="list-group-item" data-bs-theme-value="auto">
                <i class="bi bi-circle-half"></i>
            </li>
        </ul>
    </div>
    <script>
        /*!
        * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
        * Copyright 2011-2022 The Bootstrap Authors
        * Licensed under the Creative Commons Attribution 3.0 Unported License.
        */

        /** Reescrito */

        var bootstrapTheme = localStorage.getItem("theme")

        function getPreferredTheme() {
            if (bootstrapTheme) {
                return bootstrapTheme
            }

            return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
        }

        function setTheme(theme) {
            if (theme === "auto" && window.matchMedia("(prefers-color-scheme: dark)").matches) {
                document.documentElement.setAttribute("data-bs-theme", "dark")
            }
            else {
                document.documentElement.setAttribute("data-bs-theme", ((theme == "auto") ? "light" : theme))
            }
        }

        function showActiveTheme(theme) {
            $("[data-bs-theme-value]").removeClass("bg-primary text-white active")
            $(`[data-bs-theme-value="${theme}"]`).addClass("bg-primary text-white active")
        }

        $(document).on("click", '[data-bs-theme-value]', function (event) {
            const theme = this.getAttribute("data-bs-theme-value")
            localStorage.setItem("theme", theme)
            setTheme(theme)
            showActiveTheme(theme)
        })

        window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (event) {
            if (bootstrapTheme !== "light"
            || bootstrapTheme !== "dark") {
                setTheme(getPreferredTheme())
            }
        })

        document.addEventListener("DOMContentLoaded", function (event) {
            setTheme(bootstrapTheme)
            showActiveTheme(getPreferredTheme())
        })
    </script>

    <script>
        window.addEventListener("load", function (event) {
            function buscar() {
                $.get("/buscar", function (respuesta) {
                    $("#tbodyTemperaturaHumedad").html("")

                    var fechaAnterior = ""

                    for (var x in respuesta) {
                        var temperaturaHumedad = respuesta[x]

                        var fecha = ""
                        var fechaTemp = temperaturaHumedad["Fecha"]

                        if (fechaAnterior != fechaTemp) {
                            fecha         = fechaTemp
                            fechaAnterior = fechaTemp
                        }

                        $("#tbodyTemperaturaHumedad").append(`<tr>
                            <td>${temperaturaHumedad["Temperatura"]}</td>
                            <td>${temperaturaHumedad["Humedad"]}</td>
                            <td>${fecha}</td>
                            <td>${temperaturaHumedad["Hora"]}</td>
                            <td>
                                <button class="btn btn-primary btn-editar" data-id="${temperaturaHumedad["Id_Log"]}">Editar</button>
                            </td>
                        </tr>`)
                    }
                })
            }

            buscar()

            $(document).on("click", ".btn-editar", function (event) {
                var id = $(this).attr("data-id")

                $.get("/editar", {id: id}, function (respuesta) {
                    console.log(respuesta)
                    var temperaturaHumedad = respuesta[0]

                    $("#id")
                    .val(temperaturaHumedad["Id_Log"])
                    .trigger("focus")

                    $("#temperatura").val(temperaturaHumedad["Temperatura"])
                    $("#humedad").val(temperaturaHumedad["Humedad"])
                })
            })
            
            $("#frmTemperaturaHumedad")
            .submit(function (event)  {
                event.preventDefault()

                $.post("/guardar", $(this).serialize(), function (respuesta) {
                    $("#frmTemperaturaHumedad").get(0).reset()
                })
            })
            .on("reset", function (event) {
                $("#id").val("")
            })

            Pusher.logToConsole = true
            
            var pusher = new Pusher("cda1cc599395d699a2af", {
                cluster: "us2"
            })

            // Canal ---> Donde se concentran los hilos con los clientes conectados
            var channel = pusher.subscribe("canalRegistrosTemperaturaHumedad");

            // Evento --> El código que se accionará con la información enviada o el uso del canal
            channel.bind("registroTemperaturaHumedad", function (temperaturaHumedad) {
                // 1. Notificar el evento
                // alert("Ocurrió el evento")

                // 2. Recibir información enviada en el evento
                // console.log(temperaturaHumedad)

                // 3. Trabajar información enviada por el evento
                /**
                $("#tbodyTemperaturaHumedad").prepend(`<tr>
                    <td>${temperaturaHumedad.temperatura}</td>
                    <td>${temperaturaHumedad.humedad}</td>
                    <td></td>
                </tr>`)
                */

                // 4. Mandar a llamar otro código luego del evento
                buscar()
            })
        })
    </script>    
</body>
</html>
