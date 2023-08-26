$(document).ready(function () {
  hopscotch.startTour({
    id: "my-intro",
    steps: [
      {
        target: "ticket",
        title: "Raise a ticket",
        content: "Click Button and select the type of product you want to submit ticket for",
        placement: "bottom",
        yOffset: 10,
        xOffset: -105,
        arrowOffset: "center",
      },
      
    ],
    showPrevButton: !0,
  });
});
