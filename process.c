#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT
#endif


EXPORT float media(float np1, float np2, float pim){
    return ((np1*4) + (np2*4) + (pim*2)) / 10;
}

EXPORT float media_exame(float media, float exame){
    float resultado = media + exame / 2;
    return resultado > 10.0 ? 10.0 : resultado;
}

EXPORT float media_com_atividades(float np1, float np2, float pim, float soma_atividades){
    float media_base = ((np1*4) + (np2*4) + (pim*2)) / 10;
    float resultado = media_base + soma_atividades;
    return resultado > 10.0 ? 10.0 : resultado;
}