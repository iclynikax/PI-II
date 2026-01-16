//
//
//
// Verifica se a data digitada esta digitada de forma correta
$(document).ready(function() {
    $("input[name='get_Pet_dtNscmnto']").on("blur", function() {
        var dataDigitada = $(this).val();
        if (!validarFormatoData(dataDigitada)) {
            $("#mensagem").text("Formato inválido! Use DD/MM/YYYY.").css("color", "red");
            $(this).focus(); // Retorna o foco para correção
        } else if (!validarDataNaoFutura(dataDigitada)) {
            $("#mensagem").text("A data não pode ser maior que a data atual!").css("color", "red");
            $(this).focus(); // Retorna o foco para correção
        } else {
            $("#mensagem").text("Data válida!").css("color", "green");
        }
    });
});

function validarFormatoData(data) {
    var regexData = /^\d{2}\/\d{2}\/\d{4}$/; // Formato esperado: DD/MM/YYYY
    return regexData.test(data);
}

function validarDataNaoFutura(data) {
    var partes = data.split("/");
    var dataDigitada = new Date(partes[2], partes[1] - 1, partes[0]); // Ajusta para o formato Date correto
    var dataAtual = new Date();
    
    return dataDigitada <= dataAtual;
}

//================================================================================================================
// A função gerarCategorias(periodo, data) completa e inteligente, 
// que gera categorias de datas para hoje (por hora), mês (por dia) e ano (por mês), com precisão de calendário
//----------------------------------------------------------------------------------------------------------------
// ----------------------------------------------------------------------------------------------------------------------------
function gerarCategorias(tipo = 'hoje', dtRfrnca = new Date()) {
  const categorias = [];

  if (typeof dtRfrnca === "string") {
    dtRfrnca = new Date(dtRfrnca + "T00:00:00"); // força fuso local
  }

  //alert('44. [gerarCategorias] dtRfrnca in myFunctions.js: '+dtRfrnca);

  const anoDt_Ref = dtRfrnca.getFullYear();
  const mesDt_Ref = dtRfrnca.getMonth(); // zero-based
  const diaDt_Ref = dtRfrnca.getDate();

  // alert('5. diaDt_Ref: ' + diaDt_Ref);

  const dataReferencia = new Date(anoDt_Ref, mesDt_Ref, diaDt_Ref);
  // alert('6. dataReferencia: ' + dataReferencia);
      
  const ano = dataReferencia.getFullYear();
  const mes = dataReferencia.getMonth(); // zero-based
  const dia = dataReferencia.getDate();

  if (tipo === 'hoje') {
    const mesStr = String(mes + 1).padStart(2, '0');
    const diaStr = String(dia).padStart(2, '0');
    for (let h = 0; h < 25; h++) {
      const hora = String(h).padStart(2, '0');  // Configura as horas para que adequem ao fuso horário.
      categorias.push(`${ano}-${mesStr}-${diaStr}T${hora}:00:00.000Z`);
    }


  } else if (tipo === 'mes') {
    const mesStr = String(mes + 1).padStart(2, '0');
    const diasNoMes = new Date(ano, mes + 1, 0).getDate();
    for (let d = 1; d <= diasNoMes; d++) {
      const diaStr = String(d).padStart(2, '0');
      categorias.push(`${ano}-${mesStr}-${diaStr}T00:00:00.000Z`);
    }

  } else if (tipo === 'ano') {
    for (let m = 0; m < 12; m++) {
      const mesStr = String(m + 1).padStart(2, '0');
      categorias.push(`${ano}-${mesStr}-01T00:00:00.000Z`);
    }

  } else {
    console.warn(`Tipo inválido: ${tipo}. Use 'dia', 'mes' ou 'ano'.`);
  }

  return categorias;
}

//=================================================================================================================
//Exemplos de uso:                                                    Usado em:
// gerarCategorias('hoje'); // gera 24 horas de hoje                  /security/dashboard.html : renderizarGrafico   
// gerarCategorias('mes');  // gera todos os dias do mês atual
// gerarCategorias('ano');  // gera os 12 meses do ano atual
// Com data personalizada
// gerarCategorias('mes', new Date('2025-11-01'));
//------------------------------------------------------------------------------------------------------------------


function converterDataExtensoParaISO(dataExtenso) {
  const meses = {
    janeiro: "01",
    fevereiro: "02",
    março: "03",
    abril: "04",
    maio: "05",
    junho: "06",
    julho: "07",
    agosto: "08",
    setembro: "09",
    outubro: "10",
    novembro: "11",
    dezembro: "12"
  };

  const partes = dataExtenso.toLowerCase().split(" de ");
  const dia = partes[0].padStart(2, "0");
  const mes = meses[partes[1]];
  const ano = partes[2];

  return `${ano}-${mes}-${dia}`;
}


function cnvrtrMiniMsDtExtnsPraISO(dtExtenso) {
  // Converte Data de: 
  // Tue Nov 15 2025 23:32:41 GMT-0300 (Horário Padrão de Brasília)
  // Para: 
  // 2025-11-15
  //-----------------------------------------------------------------
  const meses = {
    Jan: "01",
    Fev: "02",
    mar: "03",
    Abr: "04",
    Mai: "05",
    Jun: "06",
    Jul: "07",
    Ago: "08",
    Set: "09",
    Out: "10",
    Nov: "11",
    Dez: "12"
  };

  const partes = dtExtenso.toLowerCase().split(" ");
  alert('partes: '+partes);
  const dia = partes[0].padStart(2, "0");
  const mes = meses[partes[1]];
  const ano = partes[2];

  return `${ano}-${mes}-${dia}`;
}