from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
form='<form id="form-servidor" onsubmit="salvarPerfil(event)" class="space-y-4">'
marker='<!-- FOTO DO SERVIDOR - HIDRAVIVA -->'
photo='''
                        <!-- FOTO DO SERVIDOR - HIDRAVIVA -->
                        <div class="bg-blue-50/60 border border-blue-100 rounded-2xl p-4">
                            <label class="block text-xs font-semibold text-gray-600 mb-3"><i class="fa-solid fa-camera text-seduc-lightBlue mr-1"></i> Foto do Servidor</label>
                            <div class="flex flex-col items-center">
                                <div class="relative mb-3">
                                    <div id="foto-placeholder" class="w-28 h-28 rounded-full bg-white border-4 border-white shadow-md flex items-center justify-center overflow-hidden"><i class="fa-solid fa-user text-5xl text-gray-300"></i></div>
                                    <img id="foto-preview" src="" alt="Foto do Servidor" class="hidden w-28 h-28 rounded-full object-cover border-4 border-white shadow-md">
                                    <div class="absolute bottom-0 right-0 bg-seduc-lightBlue text-white w-9 h-9 rounded-full flex items-center justify-center shadow border-2 border-white"><i class="fa-solid fa-camera text-sm"></i></div>
                                </div>
                                <p class="text-xs text-gray-500 text-center mb-3">Adicione uma foto para identificação no SEDUC HidraViva.</p>
                                <input type="file" id="input-foto" accept="image/jpeg,image/png" onchange="selecionarFotoServidor(event)" class="hidden">
                                <div class="flex flex-wrap justify-center gap-2">
                                    <button type="button" id="btn-adicionar-foto" onclick="document.getElementById('input-foto').click()" class="bg-seduc-lightBlue hover:bg-blue-700 text-white px-3 py-2 rounded-xl text-xs font-semibold transition flex items-center gap-2"><i class="fa-solid fa-image"></i> Adicionar foto</button>
                                    <button type="button" id="btn-alterar-foto" onclick="document.getElementById('input-foto').click()" class="hidden bg-gray-600 hover:bg-gray-700 text-white px-3 py-2 rounded-xl text-xs font-semibold transition flex items-center gap-2"><i class="fa-solid fa-pen"></i> Alterar</button>
                                    <button type="button" id="btn-remover-foto" onclick="removerFotoServidor()" class="hidden bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-xl text-xs font-semibold transition flex items-center gap-2"><i class="fa-solid fa-trash"></i> Remover</button>
                                </div>
                                <p class="text-[10px] text-gray-400 mt-3 text-center">Formatos permitidos: JPG, JPEG e PNG • máximo 3 MB.</p>
                            </div>
                        </div>
'''
if marker not in s:
    if form not in s: raise SystemExit('Formulario nao encontrado')
    s=s.replace(form,form+photo,1)
js_marker='// FOTO DO SERVIDOR - FUNCOES HIDRAVIVA'
save_fn='function salvarPerfil(e) {'
js='''
        // FOTO DO SERVIDOR - FUNCOES HIDRAVIVA
        function selecionarFotoServidor(event) {
            const arquivo=event.target.files&&event.target.files[0]; if(!arquivo)return;
            if(!['image/jpeg','image/png'].includes(arquivo.type)){mostrarToast('Formato não permitido. Utilize JPG, JPEG ou PNG.','error');event.target.value='';return;}
            if(arquivo.size>3*1024*1024){mostrarToast('A foto deve possuir no máximo 3 MB.','error');event.target.value='';return;}
            const leitor=new FileReader(); leitor.onload=function(ev){const img=new Image();img.onload=function(){const c=document.createElement('canvas'),ctx=c.getContext('2d'),t=400,l=Math.min(img.width,img.height),x=(img.width-l)/2,y=(img.height-l)/2;c.width=t;c.height=t;ctx.drawImage(img,x,y,l,l,0,0,t,t);perfilServidor.foto=c.toDataURL('image/jpeg',0.78);atualizarFotoServidor();salvarLocalStorage();mostrarToast('📷 Foto adicionada com sucesso!','success');};img.src=ev.target.result;}; leitor.readAsDataURL(arquivo);
        }
        function atualizarFotoServidor(){const p=document.getElementById('foto-preview'),h=document.getElementById('foto-placeholder'),a=document.getElementById('btn-adicionar-foto'),e=document.getElementById('btn-alterar-foto'),r=document.getElementById('btn-remover-foto');if(!p||!h)return;if(perfilServidor.foto){p.src=perfilServidor.foto;p.classList.remove('hidden');h.classList.add('hidden');a&&a.classList.add('hidden');e&&e.classList.remove('hidden');r&&r.classList.remove('hidden');}else{p.src='';p.classList.add('hidden');h.classList.remove('hidden');a&&a.classList.remove('hidden');e&&e.classList.add('hidden');r&&r.classList.add('hidden');}}
        function removerFotoServidor(){perfilServidor.foto='';const i=document.getElementById('input-foto');if(i)i.value='';atualizarFotoServidor();salvarLocalStorage();mostrarToast('Foto removida do cadastro.','info');}

'''
if js_marker not in s:
    if save_fn not in s: raise SystemExit('salvarPerfil nao encontrada')
    s=s.replace(save_fn,js+save_fn,1)
if 'foto: ""' not in s and "foto: ''" not in s:
    needle='cidade: "Cuiabá (Sede SEDUC/MT)",'
    if needle in s:s=s.replace(needle,needle+'\n            foto: "",',1)
if '// FOTO DO SERVIDOR - RESTAURAR AO CARREGAR' not in s:
    restore="\n<script>\n// FOTO DO SERVIDOR - RESTAURAR AO CARREGAR\nwindow.addEventListener('load',function(){try{atualizarFotoServidor();}catch(e){console.warn(e);}});\n</script>\n"
    pos=s.rfind('</body>')
    if pos<0: raise SystemExit('body nao encontrado')
    s=s[:pos]+restore+s[pos:]
s=s.replace('Desenvolvido para a Saúde e Qualidade de Vida do Servidor Público','Coordenadoria de Saúde e Segurança – CSS | SEDUC-MT')
p.write_text(s,encoding='utf-8')
print('Atualização aplicada com sucesso.')
