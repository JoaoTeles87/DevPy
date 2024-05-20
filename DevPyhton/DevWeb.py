import flet as ft

def main(pagina):
    primeira = False  # Variável de controle para mensagem inicial
    
    
   
    texto = ft.Row(
        controls=[ft.Text(spans=[ft.TextSpan("Bem vindo ao Zapzap",
                                       ft.TextStyle(size=28, weight="bold", 
                                                    foreground=ft.Paint(
                                                        gradient=ft.PaintLinearGradient(
                                                                (0, 20), (150, 20), [ft.colors.BLUE_600, ft.colors.GREEN_600]
                                        )                               
                                    ),
                                ),  
                            ),
                        ],
                    )
        ],
      alignment=ft.MainAxisAlignment.CENTER
      )
    
    chat = ft.Column()

    nomeUsuario = ft.TextField(label="Escreva seu nome")
    
   
    def enviarMensagemTunel(mensagem):
        tipo = mensagem["tipo"]
        nonlocal primeira  # Atualizar a variável de controle
        if tipo == "mensagem":
            textoEnviado = mensagem["texto"]
            usuarioEnviado = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuarioEnviado}: {textoEnviado}"))

        elif tipo == "entrada":
            usuarioEnviado = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuarioEnviado} entrou no chat", 
                                        size=12, italic=True, color=ft.colors.ORANGE_500))
            usuarioEnviado = mensagem["usuario"]     
            if not primeira:
                chat.controls.append(ft.Text(f"Olá {usuarioEnviado}! Bom te ver por aqui no chat. Sou o assistente virtual do Zapzap, ZapBolt. Divirta-se no seu bate papo!"))
                
                primeira = True
            
              
        pagina.update()
    


    pagina.pubsub.subscribe(enviarMensagemTunel)
    
    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto": campoTexto.value, "usuario": nomeUsuario.value,
                                "tipo": "mensagem"})
        campoTexto.value = ""
        pagina.update()

    campoTexto = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botaoEnviar = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_FILL_OUTLINED,
                                icon_color="blue400",
                                icon_size=20,
                                tooltip="Enviar",                           
                                on_click=enviar_mensagem)
    
    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nomeUsuario.value, "tipo": "entrada"})
        
        pagina.add(chat)
        
        popup.open = False
        
        pagina.remove(centralizarBotaoInicio)
        pagina.remove(texto)

        pagina.add(ft.Row(
            [campoTexto, botaoEnviar]
        ))
        pagina.update()

    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Bem vindo ao Zapzap"),
        content=nomeUsuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
        )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botaoInicio = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)
    centralizarBotaoInicio = ft.Row(
        controls=[botaoInicio],
        alignment=ft.MainAxisAlignment.CENTER
    )

    pagina.add(texto)
    pagina.add(centralizarBotaoInicio)


ft.app(target=main, view=ft.WEB_BROWSER, port=8000)

