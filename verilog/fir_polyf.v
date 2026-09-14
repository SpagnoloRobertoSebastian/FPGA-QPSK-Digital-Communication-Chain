//x[n] + FIR polifasico + seleccion +/-h + sumador  + salida y[n]

module fir_polyf 
//parametros
#(
    parameter OS    = 4,        //4 fases o 4 muestras por simbolo
    parameter NBAUD = 6,        //6 productos
    parameter NTAPS = 24,       //coeficientes del filtro
    parameter NB_h  = 8,       // bits totales para los coeficientes del filtro
    parameter NB_adder = 11,   // bits totales para el sumador
    parameter NB_y = 11        // bits totales para la salida y[n]
) 

//ports   
(
   output signed [NB_y   -   1  : 0]   o_yn ,     //salida del filtro FIR 

   input         i_xn    ,                        //entrada del fitro FIR
   input         EnbTx   ,                        //enable i_sw[0]
   input         i_rst   ,                        //Reset asincronico activo alto
   input         clock                            // tiempo de muestro Ts
);

//señales internas
reg         [1:0]                      fir_phase;   //fase interna del filtro polifasico 
                                                    //busca seleccionar que coeficientes del filtro se usan
reg         [NBAUD      -   1  : 0]    symbol_reg;
reg signed  [NB_h       -   1  : 0] hn [0 : NTAPS-1];
reg signed  [NB_adder   -   1  : 0] adder;

//banco de coeficientes
//Cargo los coeficientes
initial begin
    hn[0] = -8'sd1;     // -0.0078125   //guardo en entero signado en 8 bits
    hn[1] =  8'sd0;     // 0
    hn[2] =  8'sd1;     //  0.0078125
    hn[3] =  8'sd1;
    hn[4] =  8'sd0;
    hn[5] = -8'sd4;     // -0.03125
    hn[6] = -8'sd9;     // -0.0703125
    hn[7] = -8'sd9;
    hn[8] =  8'sd0;
    hn[9] =  8'sd17;    //0.1328125
    hn[10] =  8'sd41;    //0.3203125
    hn[11] =  8'sd60;    //0.46875
    hn[12] =  8'sd68;     //0.53125
    hn[13] =  8'sd60;    //0.46875
    hn[14] =  8'sd41;    //0.3203125
    hn[15] =  8'sd17;    //0.1328125
    hn[16] =  8'sd0;
    hn[17] = -8'sd9;    //-0.0703125
    hn[18] = -8'sd9;    //-0.0703125
    hn[19] = -8'sd4;    //-0.03125
    hn[20] = -8'sd1;    //-0.0078125
    hn[21] =  8'sd1;    //0.0078125
    hn[22] =  8'sd1;    //0.0078125
    hn[23] =  8'sd0;
end

//contador de fase
//00 -> fase 0
//01 -> fase 1
//10 -> fase 2
//11 -> fase 3
always @(posedge clock or posedge i_rst) begin
    if (i_rst) begin
        fir_phase <= 2'd0;
    end
    else if (EnbTx) begin
        if (fir_phase >= 2'd3) begin
            fir_phase <= 2'd0;
        end
        else  begin
          fir_phase <= fir_phase + 2'd1;    //la fase cambia por cada clock
        end  
    end      
end

//registros de simbolos x[n]
integer ptr1;
always @(posedge clock or posedge i_rst) begin
    if (i_rst) begin
        symbol_reg <= {NBAUD{1'b0}};
    end

    else if (EnbTx) begin
        // Cada 4 clocks llega un nuevo símbolo
        if (fir_phase == 2'd0) begin
            // Nuevo símbolo vine del PRBS9
            symbol_reg[0] <= i_xn;              //casa simbolo se actualiza cuando la fase es 0
                                                // o sea cada 4 ciclos de clock =Tbaudio
            // desplzo los símbolos anteriores
            for (ptr1 = 0; ptr1 < NBAUD-1; ptr1 = ptr1 + 1) begin 
                symbol_reg[ptr1+1] <= symbol_reg[ptr1];
            end
        end
    end
end


//seleccion +/- h producto, simplificando el multiplicador, el mapper y el upsample
//Seleccion es combinacional
//sumador de 6 terminos
integer ptr;  
reg signed  [NB_adder   -   1  : 0] suma;    //variable auxiliar para acomular

always @(*) begin : sel_suma
    suma = {NB_adder{1'b0}};                //inicializo el acumulador
             
    if (!i_rst && EnbTx) begin
        for (ptr = 0; ptr < NBAUD; ptr = ptr + 1) begin
            if (symbol_reg[ptr] == 1'b0)
                suma = suma + hn[ptr*OS + fir_phase];
            else
                suma = suma - hn[ptr*OS + fir_phase];
        end
    end    
    else suma={NB_adder{1'b0}};
   
    adder=suma;
end

//salida del fitro y[n] 
assign o_yn = adder;    //obtengo un valor a la salida por cada clock

endmodule

//Carga de coeficientes
//bits fraccionarios 7
//h[10]=0.3203125 ==> 0.3203125x2^7= 41 ==> h[10]=8'sd41
//(00101001)2 ==> 41 ==> 41/128 = 0.3203125