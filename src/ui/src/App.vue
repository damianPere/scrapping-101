<script setup lang="ts">
import { ref, watch, useTemplateRef } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

interface Product {
  'Calificacion promedio': string
  'Cantidad de Calificaciones': string
  'Cantidad de Opiniones': string
  Categoria: string
  Descripcion: string | null
  Descuento: boolean
  Garantia: string | null
  'Numero de Publicacion': string
  Precio: string
  Stock: string
  Titulo: string
  'URL del Producto': string
  Vendedor: string
}

const api = import.meta.env.VITE_SCRAPE
const calificacionPrecioChart = useTemplateRef('calificacionPrecioChart')
const OpinionesProductoChart = useTemplateRef('OpinionesProductoChart')
const ProductosDescuentoChart = useTemplateRef('ProductosDescuentoChart')
const data = ref<Array<Product>>([])
const loadingData = ref(false)
const dataError = ref(false)
const busqueda = ref('Portatil')
const cantidad = ref(2)

const getData = async () => {
  loadingData.value = true
  dataError.value = false
  try {
    const response = await fetch(
      `${api}/scrape?busqueda=${busqueda.value}&cantidad=${cantidad.value}`,
    )
    data.value = await response.json()
  } catch {
    dataError.value = true
  }
  loadingData.value = false
}

watch(data, () => {
  if (!data.value) {
    return null
  }
  const ChartOne = calificacionPrecioChart!.value!.getContext('2d') as CanvasRenderingContext2D
  const ChartTwo = OpinionesProductoChart!.value!.getContext('2d') as CanvasRenderingContext2D
  const ChartThree = ProductosDescuentoChart!.value!.getContext('2d') as CanvasRenderingContext2D

  // Grafica de Relacion Precio  y Calificacion
  new Chart(ChartOne, {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: 'Calificación vs Precio',
          data: data.value.map((value) => ({
            x: parseFloat(value.Precio.replace(/\./g, '')), // Reemplaza las comas por nada y convierte a número,
            y: parseFloat(value['Calificacion promedio']),
          })),
          backgroundColor: 'rgba(255, 99, 132, 1)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        x: { beginAtZero: false },
        y: { beginAtZero: true },
      },
    },
  })

  // Grafica de Opiniones
  new Chart(ChartTwo, {
    type: 'bar',
    data: {
      labels: data.value.map((opinion) => opinion.Titulo), // Títulos de productos
      datasets: [
        {
          label: 'Cantidad de Opiniones',
          data: data.value.map((opinion) => parseFloat(opinion['Cantidad de Opiniones'])), // Cantidad de opiniones
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Productos',
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Cantidad de Opiniones',
          },
        },
      },
    },
  })

  // Productos con descuento
  new Chart(ChartThree, {
    type: 'bar',
    data: {
      labels: data.value.map((producto) => producto.Titulo), // Títulos de productos
      datasets: [
        {
          label: 'Productos con Descuento',
          data: data.value.map((producto) => (producto.Descuento ? 1 : 0)), // 1 si tiene descuento, 0 si no
          backgroundColor: data.value.map((producto) =>
            producto.Descuento ? 'rgba(75, 192, 192, 0.2)' : 'rgba(255, 99, 132, 0.2)',
          ),
          borderColor: data.value.map((producto) =>
            producto.Descuento ? 'rgba(75, 192, 192, 1)' : 'rgba(255, 99, 132, 1)',
          ),
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Productos',
          },
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Con Descuento (1) / Sin Descuento (0)',
          },
        },
      },
    },
  })
})
</script>

<template>
  <main class="p-4">
    <h1 class="mb-10 text-5xl font-bold">Analisis de Datos - Grupo PREICA2402B020101</h1>
    <div class="flex gap-4 mb-20">
      <input
        v-model="busqueda"
        type="text"
        class="w-60 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        placeholder="Coloque Aquello que quiere buscar en Mercado Libre"
      />

      <input
        type="number"
        v-model="cantidad"
        min="1"
        max="5"
        placeholder="Coloque Cuantos resultados quiere buscar - Maximo 5"
        class="w-20 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
      />
      <button
        type="button"
        @click="getData"
        class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2 dark:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none dark:focus:ring-blue-800"
      >
        Obtener informacion
      </button>
    </div>
    <div v-if="dataError">Hubo un Error Cargando la informacion</div>
    <div v-if="loadingData">Cargando</div>
    <div class="flex flex-col gap-y-10">
      <div>
        <h3 class="text-xl font-bold" v-if="data && data.length > 0">Calificacion y Precio</h3>
        <canvas class="w-32! h-32!" ref="calificacionPrecioChart"></canvas>
      </div>
      <div>
        <h3 class="text-xl font-bold" v-if="data && data.length > 0">Opiniones Por Producto</h3>
        <canvas class="w-32! h-32!" ref="OpinionesProductoChart"></canvas>
      </div>
      <div>
        <h3 class="text-xl font-bold" v-if="data && data.length > 0">Producto Con Descuento</h3>
        <canvas class="w-32! h-32!" ref="ProductosDescuentoChart"></canvas>
      </div>
    </div>
  </main>
</template>
